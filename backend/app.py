import os
import uuid
import re
from flask import Flask, request, jsonify, send_file, make_response
from werkzeug.utils import secure_filename
import google.generativeai as genai
from file_handler.pdf_handler import extract_pdf_content
from file_handler.docx_handler import extract_docx_content
from file_handler.ppt_handler import extract_pptx_content
from content_processor.summarizer import summarize_content
from export_handler import export_images_and_text_to_docx, export_tables_to_docx
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()

# Configuration
STATIC_DIR = os.path.join(os.getcwd(), 'static')
UPLOAD_FOLDER = os.path.join(STATIC_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(STATIC_DIR, 'outputs')
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_FOLDER, 'sessions'), exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50*1024*1024
app.secret_key = os.environ.get("SECRET_KEY", "default-secret-key")  # For session management

# Configure Google Generative AI
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

sessions = {}
quizzes = {}

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_content(file_path):
    """Extracts text from a document based on its file type."""
    try:
        if os.path.basename(file_path).startswith("~$"):
            print(f"Skipping temporary file: {file_path}")
            return {"text": [], "images": [], "tables": []}
        
        file_type = file_path.split(".")[-1].lower()
        if file_type == "pdf":
            return extract_pdf_content(file_path)
        elif file_type == "docx":
            return extract_docx_content(file_path)
        elif file_type == "pptx":
            return extract_pptx_content(file_path)
        else:
            return {"text": [], "images": [], "tables": []}
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return {"text": [], "images": [], "tables": []}

def extract_from_files(file_paths):
    """Extracts content from all valid files and formats it for chatbot use."""
    all_text = ""
    for file_path in file_paths:
        if os.path.isfile(file_path):
            print(f"Processing: {os.path.basename(file_path)} ...")
            content = extract_content(file_path)
            for page_text in content["text"]:
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

def query_gemini(document_text, user_query):
    """Queries Gemini API with the document text and user query."""
    prompt = f"Based on the documents:\n\n{document_text}\n\nAnswer: {user_query}"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running"""
    return jsonify({
        "status": "healthy", 
        "message": "Document processing API is running",
        "service": "Document Processing API",
        "active_sessions": len(sessions),
        "stored_quizzes": len(quizzes)
    }), 200

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """API endpoint to upload files and append extracted content to an existing session"""
    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({"error": "No files selected"}), 400
    # Get session ID from request header or create a new one
    session_id = request.headers.get("X-Session-ID")
    new_session = False
    if session_id not in sessions.keys():
        session_id = str(uuid.uuid4())
        new_session = True
        sessions[session_id] = {
            "files": [],
            "file_names": [],
            "text_content": "",
            "uploaded_files": []
        }
    new_file_paths = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
            file.save(file_path)
            sessions[session_id]["files"].append(file_path)
            sessions[session_id]["file_names"].append(filename)
            sessions[session_id]["uploaded_files"].append({"id": str(uuid.uuid4()), "name": filename})
            new_file_paths.append(file_path)
    # Extract content only from new files and append it to existing content
    new_text = extract_from_files(new_file_paths) if new_file_paths else ""
    if new_text:
        sessions[session_id]["text_content"] += ("\n" + new_text) if sessions[session_id]["text_content"] else new_text
    response = make_response(jsonify({
        "session_id": session_id,
        "message": "Files uploaded and processed successfully",
        "files": sessions[session_id]["uploaded_files"],
        "has_content": bool(sessions[session_id]["text_content"])
    }))
    return response

@app.route('/api/process/<session_id>', methods=['POST'])
def process_documents(session_id):
    """
    Process all documents in a session and generate consolidated outputs
    """
    session_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'sessions', session_id)
    
    if not os.path.exists(session_dir):
        return jsonify({"error": f"Session {session_id} not found"}), 404
    
    all_content = {"text": [], "tables": [], "images": []}
    
    # Process each file in the session directory
    for file_info in sessions[session_id]["files"]:
        file_path = file_info["path"]
        filename = file_info["filename"]
        
        try:
            if filename.endswith(".pdf"):
                content = extract_pdf_content(file_path)
            elif filename.endswith(".docx"):
                content = extract_docx_content(file_path)
            elif filename.endswith(".pptx"):
                content = extract_pptx_content(file_path)
            else:
                continue  # Skip unsupported files
            
            # Append extracted content
            all_content["text"].extend(content["text"])
            all_content["tables"].extend(content["tables"])
            all_content["images"].extend(content["images"])
            
        except Exception as e:
            return jsonify({
                "error": f"Error processing file {filename}",
                "details": str(e)
            }), 500
    
    if not all_content["text"]:
        return jsonify({"error": "No content was extracted from the uploaded files"}), 400
    
    try:
        # Summarize the text content
        all_content["text"] = summarize_content(all_content["text"])
        
        # Generate consolidated output files
        consolidated_doc_path = os.path.join(output_dir, "consolidated_notes.docx")
        tables_doc_path = os.path.join(output_dir, "consolidated_tables.docx")
        
        export_images_and_text_to_docx(all_content, consolidated_doc_path)
        export_tables_to_docx(all_content, tables_doc_path)
        
        return jsonify({
            "status": "success",
            "session_id": session_id,
            "message": "Documents processed successfully",
            "consolidated_doc": f"/api/download/{session_id}/notes",
            "tables_doc": f"/api/download/{session_id}/tables"
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "Error during document consolidation",
            "details": str(e)
        }), 500

@app.route('/api/download/<session_id>/<file_type>', methods=['GET'])
def download_file(session_id, file_type):
    """
    Download the consolidated document or tables document
    """
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'sessions', session_id)
    
    if not os.path.exists(output_dir):
        return jsonify({"error": f"Session {session_id} not found"}), 404
    
    if file_type == "notes":
        file_path = os.path.join(output_dir, "consolidated_notes.docx")
        file_name = "consolidated_notes.docx"
    elif file_type == "tables":
        file_path = os.path.join(output_dir, "consolidated_tables.docx")
        file_name = "consolidated_tables.docx"
    else:
        return jsonify({"error": "Invalid file type requested"}), 400
    
    if not os.path.exists(file_path):
        return jsonify({"error": f"Requested file not found"}), 404
    
    return send_file(
        file_path,
        as_attachment=True,
        download_name=file_name,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

@app.route('/api/query', methods=['POST'])
def query_chatbot():
    """API endpoint to query the chatbot"""
    data = request.json
    
    if not data or "session_id" not in data or "query" not in data:
        return jsonify({"error": "Missing session_id or query"}), 400
    
    session_id = data["session_id"]
    user_query = data["query"]
    
    if session_id not in sessions:
        return jsonify({"error": "Invalid or expired session ID"}), 404
    
    document_text = sessions[session_id]["text_content"]
    if not document_text:
        return jsonify({"error": "No document content available"}), 400
    
    # Query Gemini with document text and user query
    response = query_gemini(document_text, user_query)
    
    return jsonify({
        "response": response
    })

@app.route('/api/generate-quiz', methods=['POST'])
def create_quiz():
    """API endpoint to generate a quiz"""
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Extract parameters
    session_id = data.get("session_id")
    topic = data.get("topic", "")
    difficulty = data.get("difficulty", "medium")
    num_questions = data.get("numberOfQuestions", 10)
    
    if not session_id:
        return jsonify({"error": "Session ID is required"}), 400
    
    if session_id not in sessions:
        return jsonify({"error": "Invalid or expired session ID"}), 404
    
    # Use the already extracted text content
    document_text = sessions[session_id]["text_content"]
    
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

@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """Retrieve session information"""
    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 404
    
    # Check if the output files have been generated
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'sessions', session_id)
    consolidated_doc_path = os.path.join(output_dir, "consolidated_notes.docx")
    tables_doc_path = os.path.join(output_dir, "consolidated_tables.docx")
    
    processing_complete = (
        os.path.exists(consolidated_doc_path) and
        os.path.exists(tables_doc_path)
    )
    
    # Return session info
    session_info = {
        "session_id": session_id,
        "files": sessions[session_id]["file_names"],
        "has_content": bool(sessions[session_id]["text_content"]),
        "status": "complete" if processing_complete else "pending",
        "downloads": {
            "consolidated_doc": f"/api/download/{session_id}/notes" if processing_complete else None,
            "tables_doc": f"/api/download/{session_id}/tables" if processing_complete else None
        }
    }
    
    return jsonify(session_info)

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout endpoint that clears user's session and associated files"""
    data = request.json
    
    if not data or "session_id" not in data:
        return jsonify({"error": "Session ID is required"}), 400
    
    session_id = data["session_id"]
    
    if session_id not in sessions:
        return jsonify({"message": "No active session found"}), 200
    
    # Delete all files in the session directory
    session_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    if os.path.exists(session_dir):
        for file in os.listdir(session_dir):
            file_path = os.path.join(session_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        try:
            os.rmdir(session_dir)
            print(f"Deleted directory: {session_dir}")
        except Exception as e:
            print(f"Error deleting directory {session_dir}: {e}")
    
    # Delete output files
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'sessions', session_id)
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted output file: {file_path}")
            except Exception as e:
                print(f"Error deleting output file {file_path}: {e}")
        try:
            os.rmdir(output_dir)
            print(f"Deleted output directory: {output_dir}")
        except Exception as e:
            print(f"Error deleting output directory {output_dir}: {e}")
    
    # Delete any quizzes associated with this session
    quiz_ids_to_delete = []
    for quiz_id, quiz_data in quizzes.items():
        if quiz_data["metadata"]["session_id"] == session_id:
            quiz_ids_to_delete.append(quiz_id)
    
    for quiz_id in quiz_ids_to_delete:
        del quizzes[quiz_id]
        print(f"Deleted quiz: {quiz_id}")
    
    # Remove session data
    del sessions[session_id]
    print(f"Deleted session: {session_id}")
    
    return jsonify({"message": "Logged out successfully. All session data and files have been cleared."})

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)