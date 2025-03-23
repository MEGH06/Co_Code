from file_handler.pdf_handler import extract_pdf_content
from file_handler.docx_handler import extract_docx_content
from file_handler.ppt_handler import extract_pptx_content
from content_processor.summarizer import summarize_content
from export_handler import export_images_and_text_to_docx, export_tables_to_docx
import os

def process_file(file_path):
    """Process a single file and return its content"""
    if file_path.endswith(".pdf"):
        return extract_pdf_content(file_path)
    elif file_path.endswith(".docx"):
        return extract_docx_content(file_path)
    elif file_path.endswith(".pptx"):
        return extract_pptx_content(file_path)
    else:
        print(f"Unsupported file type: {file_path}")
        return {"text": [], "tables": [], "images": []}

def process_multiple_files(file_paths):
    """Process multiple files and return combined content"""
    all_content = {"text": [], "tables": [], "images": []}
    
    for file_path in file_paths:
        if os.path.exists(file_path):
            content = process_file(file_path)
            # Append extracted content to the combined dictionary
            all_content["text"].extend(content["text"])
            all_content["tables"].extend(content["tables"])
            all_content["images"].extend(content["images"])
        else:
            print(f"File not found: {file_path}")
    
    return all_content

def main(file_paths):
    # Process all provided files
    all_content = process_multiple_files(file_paths)
    
    # Summarize the combined text
    all_content["text"] = summarize_content(all_content["text"])
    
    # Export two documents
    export_images_and_text_to_docx(all_content)  # One with summarized text and relevant images
    export_tables_to_docx(all_content)  # Another with all tables
    
    print("Processing complete. Documents exported successfully.")

if __name__ == "__main__":
    # Example usage with command line arguments
    import sys
    if len(sys.argv) < 2:
        print("Usage: python script.py file1.pdf file2.docx file3.pptx")
        sys.exit(1)
    
    # Get file paths from command line arguments
    file_paths = sys.argv[1:]
    main(file_paths)

# from file_handler.pdf_handler import extract_pdf_content
# from file_handler.docx_handler import extract_docx_content
# from file_handler.ppt_handler import extract_pptx_content
# from content_processor.summarizer import summarize_content
# from export_handler import export_images_and_text_to_docx, export_tables_to_docx
# import os

# def main():
#     input_dir = "./uploaded_files"
#     all_content = {"text": [], "tables": [], "images": []}
#     # Process files
#     for filename in os.listdir(input_dir):
#         file_path = os.path.join(input_dir, filename)
#         if filename.endswith(".pdf"):
#             content = extract_pdf_content(file_path)
#         elif filename.endswith(".docx"):
#             content = extract_docx_content(file_path)
#         elif filename.endswith(".pptx"):
#             content = extract_pptx_content(file_path)
#         else:
#             print(f"Unsupported file type: {filename}")
#             continue
#         # appending extracted content from all documents into one dictionary
#         all_content["text"].extend(content["text"])
#         all_content["tables"].extend(content["tables"])
#         all_content["images"].extend(content["images"])
    
#     all_content["text"] = summarize_content(all_content["text"]) # summarizing the text and storing in the same dictionary
#     # exporting 2 documents
#     export_images_and_text_to_docx(all_content) # one with summarized text and relevant images
#     export_tables_to_docx(all_content) # and another with all tables

# if __name__ == "__main__":
#     main()