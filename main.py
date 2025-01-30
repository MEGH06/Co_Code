from file_handler.pdf_handler import extract_pdf_content
from file_handler.docx_handler import extract_docx_content
from file_handler.ppt_handler import extract_pptx_content
from content_processor.merger import merge_content
from output_generator.export_handler import export_to_docx
import os
def main():
    # Directory containing uploaded files
    input_dir = "./uploaded_files"
    consolidated_content = {"text": [], "tables": [], "images": []}
    # Process files
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if filename.endswith(".pdf"):
            content = extract_pdf_content(file_path)
        elif filename.endswith(".docx"):
            content = extract_docx_content(file_path)
        elif filename.endswith(".pptx"):
            content = extract_ppt_content(file_path)
        else:
            print(f"Unsupported file type: {filename}")
            continue
        # Append extracted content
        consolidated_content["text"].extend(content["text"])
        consolidated_content["tables"].extend(content["tables"])
        consolidated_content["images"].extend(content["images"])
    # Merge and process content
    final_content = merge_content(consolidated_content)
    # Export final content
    output_path = "./output/consolidated_notes.docx"
    export_to_docx(final_content, output_path)
    print(f"Consolidated document saved at: {output_path}")
if __name__ == "__main__":
    main()