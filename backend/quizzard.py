from flask import Flask, request, jsonify
import os
import json
import uuid
import re
import google.generativeai as genai
from werkzeug.utils import secure_filename
from file_handler.docx_handler import extract_docx_content
from file_handler.ppt_handler import extract_pptx_content
from file_handler.pdf_handler import extract_pdf_content
from flask_cors import CORS
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploaded_files'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'pptx'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

load_dotenv()
# Configure Google Generative AI
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# In-memory storage for session data and generated quizzes
sessions = {}
quizzes = {}

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_content(file_path):
    """Extracts text from a document based on its file type."""
    try:
        if os.path.basename(file_path).startswith("~$"):
            print(f"Skipping temporary file: {file_path}")
            return {"text": []}
        
        file_type = file_path.split(".")[-1].lower()
        if file_type == "pdf":
            return extract_pdf_content(file_path)
        elif file_type == "docx":
            return extract_docx_content(file_path)
        elif file_type == "pptx":
            return extract_pptx_content(file_path)
        else:
            return {"text": []}
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return {"text": []}

def extract_from_files(file_paths):
    """Extracts content from all valid files."""
    all_text = ""
    for file_path in file_paths:
        if os.path.isfile(file_path):
            print(f"Processing: {os.path.basename(file_path)} ...")
            text = extract_content(file_path)["text"]
            for page_text in text:
                if page_text.strip():
                    all_text += f"\n\n=== {os.path.basename(file_path)} ===\n{page_text}"
    return all_text.strip()

def parse_mcq_output(mcq_text):
    """Parse the MCQ output from Gemini API into structured format."""
    # Extract questions and options
    question_pattern = re.findall(r"(\d+)\.\s+(.*?)\n\s*a\)\s+(.*?)\n\s*b\)\s+(.*?)\n\s*c\)\s+(.*?)\n\s*d\)\s+(.*?)(?:\n|$)", mcq_text, re.DOTALL)
    
    questions = []
    for num, question, option_a, option_b, option_c, option_d in question_pattern:
        questions.append({
            "id": int(num) - 1,  # Convert to 0-indexed
            "question": question.strip(),
            "options": [
                option_a.strip(),
                option_b.strip(),
                option_c.strip(),
                option_d.strip()
            ]
        })
    
    # Extract answers
    answer_pattern = re.search(r"\{(.*?)\}", mcq_text, re.DOTALL)
    correct_answers = {}
    
    if answer_pattern:
        answer_text = answer_pattern.group(1)
        # Convert letter answers (a,b,c,d) to numeric (0,1,2,3)
        answer_entries = re.findall(r'"(\d+)":\s*"([a-d])"', answer_text)
        
        for q_num, ans_letter in answer_entries:
            q_index = int(q_num) - 1  # Convert to 0-indexed
            correct_index = ord(ans_letter) - ord('a')  # Convert letter to index (a=0, b=1, etc.)
            correct_answers[q_index] = correct_index
    
    # Assign correct answers to questions
    for question in questions:
        q_id = question["id"]
        if q_id in correct_answers:
            question["correctAnswer"] = correct_answers[q_id]
        else:
            # Default to first option if answer not found
            question["correctAnswer"] = 0
    
    return questions

def generate_quiz(document_text, topic, difficulty, num_questions):
    """Generate MCQ quiz using Gemini API."""
    difficulty_prompts = {
        "easy": "Make these questions relatively easy, focusing on basic concepts and explicit information from the document.",
        "medium": "Make these questions moderately challenging, requiring some understanding and inference from the document.",
        "hard": "Make these questions challenging, requiring deeper analysis and understanding of concepts in the document.",
        "extreme": "Make these questions very challenging, requiring synthesis of multiple concepts and critical thinking."
    }
    
    difficulty_guidance = difficulty_prompts.get(difficulty, difficulty_prompts["medium"])
    topic_guidance = f"Focus primarily on the topic of '{topic}'. " if topic else ""
    
    user_query = (
        "Based on the following document, generate exactly {num} multiple-choice questions.\n\n"
        "{topic_guidance}"
        "{difficulty_guidance}\n\n"
        "Format the output exactly as follows:\n\n"
        "### Questions:\n"
        "1. Question text here?\n"
        "   a) Option 1\n"
        "   b) Option 2\n"
        "   c) Option 3\n"
        "   d) Option 4\n\n"
        "2. Question text here?\n"
        "   a) Option 1\n"
        "   b) Option 2\n"
        "   c) Option 3\n"
        "   d) Option 4\n\n"
        "...(continue for all questions)\n\n"
        "### Answers:\n"
        "{{ \"1\": \"b\", \"2\": \"d\", \"3\": \"a\", ..., \"{num}\": \"c\" }}\n\n"
        "Ensure that:\n"
        "- Each question has 4 answer choices labeled (a, b, c, d).\n"
        "- The correct answer should be provided in the JSON dictionary format separately.\n"
        "- Do not add extra text, explanations, or formatting beyond the requested structure."
    ).format(
        num=num_questions,
        topic_guidance=topic_guidance,
        difficulty_guidance=difficulty_guidance
    )
    
    prompt = f"Based on the following document:\n\n{document_text}\n\n{user_query}"
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    return response.text if response else "No response from Gemini."

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """API endpoint to upload files"""
    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({"error": "No files selected"}), 400
    
    # Create a new session
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"files": [], "file_names": []}
    
    # Process each file
    uploaded_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
            file.save(file_path)
            
            sessions[session_id]["files"].append(file_path)
            sessions[session_id]["file_names"].append(filename)
            uploaded_files.append({"id": str(uuid.uuid4()), "name": filename})
    
    return jsonify({
        "session_id": session_id, 
        "message": "Files uploaded and processed successfully",
        "files": uploaded_files
    })

@app.route('/api/generate-quiz', methods=['POST'])
def create_quiz():
    """API endpoint to generate a quiz"""
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Extract parameters
    session_id = data.get("session_id")
    file_ids = data.get("fileid", [])
    topic = data.get("topic", "")
    difficulty = data.get("difficulty", "medium")
    num_questions = data.get("numberOfQuestions", 10)
    
    if not session_id:
        return jsonify({"error": "Session ID is required"}), 400
    
    if session_id not in sessions:
        return jsonify({"error": "Invalid or expired session ID"}), 404
    
    # Extract content from specified files (or all files if none specified)
    if not file_ids:
        file_paths = sessions[session_id]["files"]
    else:
        # In a real implementation, you would map file_ids to actual file paths
        # For simplicity, we'll just use all files in the session
        file_paths = sessions[session_id]["files"]
    
    document_text = extract_from_files(file_paths)
    
    if not document_text:
        return jsonify({"error": "No content could be extracted from the documents"}), 400
    
    # Generate quiz
    mcq_output = generate_quiz(document_text, topic, difficulty, num_questions)
    questions = parse_mcq_output(mcq_output)
    
    # Store the quiz
    quiz_id = str(uuid.uuid4())
    quizzes[quiz_id] = {
        "questions": questions,
        "metadata": {
            "topic": topic,
            "difficulty": difficulty,
            "num_questions": num_questions,
            "session_id": session_id
        }
    }
    
    return jsonify({
        "quiz_id": quiz_id,
        "questions": questions
    })

@app.route('/api/quiz/<quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """API endpoint to retrieve a generated quiz"""
    if quiz_id not in quizzes:
        return jsonify({"error": "Quiz not found"}), 404
    
    return jsonify({
        "quiz_id": quiz_id,
        "questions": quizzes[quiz_id]["questions"],
        "metadata": quizzes[quiz_id]["metadata"]
    })

@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """List all active sessions"""
    session_list = []
    for session_id, session_data in sessions.items():
        session_list.append({
            "session_id": session_id,
            "files": session_data["file_names"],
            "file_count": len(session_data["files"])
        })
    
    return jsonify({"sessions": session_list})

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a session and its files"""
    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 404
    
    # Delete uploaded files
    for file_path in sessions[session_id]["files"]:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    
    # Remove session data
    del sessions[session_id]
    
    # Also delete any quizzes associated with this session
    quiz_ids_to_delete = []
    for quiz_id, quiz_data in quizzes.items():
        if quiz_data["metadata"]["session_id"] == session_id:
            quiz_ids_to_delete.append(quiz_id)
    
    for quiz_id in quiz_ids_to_delete:
        del quizzes[quiz_id]
    
    return jsonify({"message": "Session and associated quizzes deleted successfully"})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok", "service": "Quizzard API"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='localhost', port=port, debug=True)