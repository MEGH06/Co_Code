from file_handler.pdf_handler import extract_pdf_content
from file_handler.docx_handler import extract_docx_content
from file_handler.ppt_handler import extract_pptx_content
from content_processor.summarizer import summarize_content
from export_handler import export_images_and_text_to_docx, export_tables_to_docx
import os

def main():
    input_dir = "./uploaded_files"
    all_content = {"text": [], "tables": [], "images": []}
    # Process files
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if filename.endswith(".pdf"):
            content = extract_pdf_content(file_path)
        elif filename.endswith(".docx"):
            content = extract_docx_content(file_path)
        elif filename.endswith(".pptx"):
            content = extract_pptx_content(file_path)
        else:
            print(f"Unsupported file type: {filename}")
            continue
        # appending extracted content from all documents into one dictionary
        all_content["text"].extend(content["text"])
        all_content["tables"].extend(content["tables"])
        all_content["images"].extend(content["images"])
    
    all_content["text"] = summarize_content(all_content["text"]) # summarizing the text and storing in the same dictionary
    # exporting 2 documents
    export_images_and_text_to_docx(all_content) # one with summarized text and relevant images
    export_tables_to_docx(all_content) # and another with all tables

if __name__ == "__main__":
    main()