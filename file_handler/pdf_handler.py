import fitz
import pytesseract
from PIL import Image
import io
# import camelot # type: ignore

def extract_pdf_content(pdf_file):
    # Will be used to extract text, images and tables from a pdf document
    # Will also be used to extract text, images and tables from a scanned PDF using OCR
    pdf_content = {
        "text": [],
        "images": [],
        "tables": []
    }
    document = fitz.open(pdf_file)
    for page_num, page in enumerate(document):
        page_text = page.get_text() # extracting text from the pdf
        if page_text.strip():  # If text exists, PDF is processed as text-based
            pdf_content["text"].append(page_text)
            # try:
            #     tables = camelot.read_file(pdf_file,pages=str(page_num+1),flavor="stream")
            #     for table in tables:
            #         pdf_content["tables"].append(table.df.values.to_list())
            # except Exception as e:
            #     print(f"No tables found on page {page_num + 1}: {e}")
        else:
            # If no text, process as scanned PDF using OCR
            pix = page.get_pixmap()  # Render page to an image
            img = Image.open(io.BytesIO(pix.tobytes()))
            ocr_text = pytesseract.image_to_string(img)
            pdf_content["text"].append(ocr_text)
        
        for img_index, img in enumerate(page.get_images(full=False)):
            xref = img[0]
            base_image = document.extract_image(xref)
            img_bytes = base_image["image"]
            img_filename = f"{pdf_file}_page{page_num}_img{img_index}.png"
            with open(img_filename, "wb") as img_file:
                img_file.write(img_bytes)
            pdf_content["images"].append(img_filename)
    document.close()
    return pdf_content

output = extract_pdf_content("/Users/kashishmandhane/Documents/Kashish Data/LAPTOP STUFF/DJ Sanghvi College/Extra-curriculars/Hackathons/Ed-tech/Hackathon Announcement_ DJS Compute.pdf")
print(output["text"])
print(output["images"])
