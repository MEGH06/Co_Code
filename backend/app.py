import os
import json
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import google.generativeai as genai
from file_handler.docx_handler import extract_docx_content
from file_handler.ppt_handler import extract_pptx_content
from file_handler.pdf_handler import extract_pdf_content
from warnings import warn
from dotenv import load_dotenv


app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploaded_files'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'pptx'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

load_dotenv()
# Configure Google Generative AI
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# In-memory storage for session data
sessions = {}

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_content(file_path):
    """Extracts text from a document based on its file type."""
    try:
        if os.path.basename(file_path).startswith("~$"):
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

def query_gemini(document_text, user_query):
    """Queries Gemini API with the document text and user query."""
    prompt = f"Based on the documents:\n\n{document_text}\n\nAnswer: {user_query}"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

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
    sessions[session_id] = {"files": [], "text_content": ""}
    
    # Process each file
    all_text = ""
    uploaded_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
            file.save(file_path)
            
            # Extract content
            content = extract_content(file_path)
            for page_text in content["text"]:
                if page_text.strip():
                    all_text += f"\n\n=== {filename} ===\n{page_text}"
            
            uploaded_files.append(filename)
            sessions[session_id]["files"].append(file_path)
    
    # Store extracted text in session data
    sessions[session_id]["text_content"] = all_text.strip()
    
    return jsonify({
        "session_id": session_id, 
        "message": "Files uploaded and processed successfully",
        "files": uploaded_files
    })

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

@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """Retrieve session information"""
    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 404
    
    # Return session info without the full text content
    session_info = {
        "session_id": session_id,
        "files": [os.path.basename(f) for f in sessions[session_id]["files"]],
        "has_content": bool(sessions[session_id]["text_content"])
    }
    
    return jsonify(session_info)

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
    
    return jsonify({"message": "Session deleted successfully"})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='localhost', port=port, debug=True)