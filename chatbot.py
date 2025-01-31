import os
import google.generativeai as genai
from file_handler.docx_handler import extract_docx_content
from file_handler.ppt_handler import extract_pptx_content
from file_handler.pdf_handler import extract_pdf_content

# Configure Gemini API (Replace with your API key)
genai.configure(api_key="API_KEY")

def extract_content(file_path):
    """Extracts text from a given document based on its file type."""
    try:
        # Skip temporary or system files starting with '~$'
        if os.path.basename(file_path).startswith("~$"):
            print(f"Skipping temporary file: {file_path}")
            return {"text":[], "images": [], "tables": []}  # Return empty string if it's a temp file
        file_type = file_path.split(".")[-1].lower()
        if file_type == "pdf":
            return extract_pdf_content(file_path)
        elif file_type == "docx":
            return extract_docx_content(file_path)
        elif file_type == "pptx":
            return extract_pptx_content(file_path)
        else:
            return {"text":[], "images": [], "tables": []}  # Ignore unsupported files
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return {"text":[], "images": [], "tables": []}  # Return empty string on error

def extract_from_folder(folder_path):
    """Extracts content from all valid files in a given folder."""
    all_text = ""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith((".pdf", ".docx", ".pptx")):
            print(f"Processing: {file_name} ...")
            text = extract_content(file_path)["text"]
            for page_text in text:
                if page_text.strip():
                    all_text += f"\n\n=== {file_name} ===\n{page_text}"
    print(all_text)
    return all_text.strip()

def query_gemini_api(document_text, user_query):
    """Queries the Gemini API using the extracted document text and user query."""
    prompt = f"Based on the following documents:\n\n{document_text}\n\nAnswer this query: {user_query}"
    
    model = genai.GenerativeModel("gemini-pro")  # Change model if needed
    response = model.generate_content(prompt)

    return response.text if response else "No response from Gemini."

def chatbot():
    """Main function to interact with the chatbot."""
    folder_path = input("Enter the path to the folder containing documents: ").strip()

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print("Error: Folder not found.")
        return
    
    print("Extracting content from all files... Please wait.")
    document_text = extract_from_folder(folder_path)

    if not document_text:
        print("Error: No text extracted from the documents.")
        return
    
    print("\nAll documents processed. You can now ask questions.")

    while True:
        user_query = input("\nAsk a question (or type 'exit' to quit): ").strip()
        if user_query.lower() == "exit":
            print("Goodbye!")
            break

        response = query_gemini_api(document_text, user_query)
        print("\nChatbot: ", response)

# Run the chatbot
if __name__ == "__main__":
    chatbot()
