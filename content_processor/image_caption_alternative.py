import pytesseract
from PIL import Image
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from fpdf import FPDF

# Load SentenceTransformer model and Summarization Pipeline
model = SentenceTransformer('all-MiniLM-L6-v2')
summarizer = pipeline("summarization")

# Step 1: Extract Text from Images
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}")
        return ""

# Step 2: Deduplicate Text
def deduplicate_text(text_list):
    unique_text = []
    embeddings = model.encode(text_list, convert_to_tensor=True)
    for i, text in enumerate(text_list):
        is_duplicate = False
        for j in range(i):
            similarity = util.cos_sim(embeddings[i], embeddings[j])
            if similarity > 0.9:  # Threshold for duplication
                is_duplicate = True
                break
        if not is_duplicate:
            unique_text.append(text)
    return unique_text

# Step 3: Generate Summary
def generate_summary(text):
    try:
        if len(text) < 20:
            return text  # Avoid summarizing very short text
        summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error generating summary: {e}")
        return text

# Step 4: Chunk the Summary
def chunk_summary(summary, chunk_size=100):
    words = summary.split()
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# Step 5: Perform Semantic Matching
def match_images_with_chunks(chunks, captions):
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)
    caption_embeddings = model.encode(captions, convert_to_tensor=True)
    matches = []
    for chunk_idx, chunk_embedding in enumerate(chunk_embeddings):
        best_match = None
        best_similarity = 0
        for caption_idx, caption_embedding in enumerate(caption_embeddings):
            similarity = util.cos_sim(chunk_embedding, caption_embedding)
            if similarity > best_similarity:
                best_match = caption_idx
                best_similarity = similarity
        matches.append((chunk_idx, best_match))
    return matches

# Step 6: Generate Final PDF
def generate_pdf(output_path, chunks, images, matches):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for chunk_idx, chunk in enumerate(chunks):
        pdf.multi_cell(0, 10, chunk.encode('latin-1', 'replace').decode('latin-1'))  # Handle unsupported characters
        pdf.ln(5)
        # Add matched image
        for match in matches:
            if match[0] == chunk_idx and match[1] is not None:
                image_path, caption = images[match[1]]
                try:
                    pdf.image(image_path, w=100)  # Adjust image size as needed
                    pdf.ln(5)
                    pdf.cell(0, 10, f"Caption: {caption}", ln=True)
                    pdf.ln(10)
                except Exception as e:
                    print(f"Error adding image {image_path} to PDF: {e}")
    pdf.output(output_path)

# Example Workflow
if __name__ == "__main__":
    # Example data
    images = [
        ("../image1.png", "Caption for image 1"),
        ("../image2.png", "Caption for image 2"),
    ]
    raw_text = "This is the raw extracted text from documents and images."
    
    # Step 1: Extract text (example from images)
    extracted_text = [extract_text_from_image(image[0]) for image in images]
    
    # Step 2: Deduplicate text and captions
    all_text = [raw_text] + extracted_text + [caption for _, caption in images]
    deduplicated_text = deduplicate_text(all_text)
    
    # Step 3: Generate summary
    summary = generate_summary(" ".join(deduplicated_text))
    
    # Step 4: Chunk the summary
    chunks = chunk_summary(summary, chunk_size=50)
    
    # Step 5: Match images with text chunks
    captions = [caption for _, caption in images]
    matches = match_images_with_chunks(chunks, captions)
    
    # Step 6: Generate final PDF
    generate_pdf("output.pdf", chunks, images, matches)

    print("PDF generated successfully!")