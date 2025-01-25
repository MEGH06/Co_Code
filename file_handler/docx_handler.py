from docx import Document
import os
import zipfile

def extract_docx_content(file_path):
    """Extract text, tables, and images from a Word document."""
    content = {"text": [], "tables": [], "images": []}
    doc = Document(file_path)

    # Extract text
    for para in doc.paragraphs:
        if para.text.strip():  # Skip empty paragraphs
            content["text"].append(para.text.strip())

    # Extract tables
    for table in doc.tables:
        table_data = [[cell.text.strip() for cell in row.cells] for row in table.rows]
        content["tables"].append(table_data)

    return content

def extract_images(file_path, output_dir="images"):
    """Extract images from a Word document."""
    with zipfile.ZipFile(file_path, 'r') as docx:
        media_files = [f for f in docx.namelist() if f.startswith('word/media/')]
        os.makedirs(output_dir, exist_ok=True)
        for media in media_files:
            with open(os.path.join(output_dir, os.path.basename(media)), 'wb') as img_file:
                img_file.write(docx.read(media))
        return [os.path.join(output_dir, os.path.basename(media)) for media in media_files]

# Example usage
file_path = r"C:\Users\Kruttika\OneDrive\Desktop\Kruttika\Report Format.docx"
content = extract_docx_content(file_path)
images = extract_images(file_path)
content["images"] = images


print("Text Content:", content["text"])
print("Tables:", content["tables"])
print("Images Extracted:", content["images"])

