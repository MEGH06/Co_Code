# Bytecoders - File Consolidation and Handling

## Project Overview

The main goal of this project is to develop a system where users can upload files such as PDFs, Word documents (DOCX), or PowerPoint presentations (PPTs). Using **Natural Language Processing (NLP)**, the system will consolidate the content from these files into a single, streamlined document. This consolidated document will contain all the essential information while removing redundant or repeated parts, making it more concise and easier to read.

Additionally, the project includes a **Retrieval-Augmented Generation (RAG)-based chatbot** that interacts with the user, allowing them to ask questions about the consolidated content. 

The final system will be deployed using **Docker** for environment consistency and **Vercel** for hosting.

## Key Features

- **File Upload**: Users can upload PDFs, DOCX, or PPT files.
- **Text Extraction**: Automatically extract text content from uploaded files.
- **Consolidation**: Merge content from multiple files into a single document, removing redundant information.
- **RAG-based Chatbot**: A chatbot that answers questions based on the consolidated document.
- **Diagram and Table Handling**: Extract and store diagrams and tables from the files.
- **Deployment**: Docker for packaging and Vercel for hosting the system.

## Deployment

- **Docker**: Ensures that the system runs consistently across different environments by packaging the application and all its dependencies into a container.
- **Vercel**: Provides a simple web interface to upload files and retrieve the consolidated document.

## Implementation Details

### 1. File-Type-Specific Preprocessing

#### 1.1 PDFs
- **Extraction Tool**: PyPDF2, pdfplumber, PyMuPDF
- **Steps**:
  - Extract text content while maintaining order.
  - Handle multi-column PDFs and layout patterns.
  - Extract metadata (title, author, date).
  - Handle diagrams/images and store separately.
  - Extract tables using camelot or tabula-py.
  
#### 1.2 DOCX (Word Documents)
- **Extraction Tool**: python-docx
- **Steps**:
  - Parse text, including headings, paragraphs, and lists.
  - Retain emphasis (bold, italicized, underlined text).
  - Extract tables and images.
  - Handle footnotes/endnotes and append them as references.

#### 1.3 PPT (PowerPoint Presentations)
- **Extraction Tool**: python-pptx
- **Steps**:
  - Extract text from slides, titles, bullet points, and speaker notes.
  - Extract images/diagrams.
  - Handle tables and retain slide structure.

### 2. Handling Specific Elements

#### 2.1 Diagrams
- **Extraction**: Use PyMuPDF, python-docx, python-pptx.
- **OCR**: Use Tesseract for text extraction from diagrams.
- **Reintegration**: Add placeholders (e.g., [Diagram 1]) in the consolidated document.

#### 2.2 Tables
- **Extraction**: Use camelot/tabula-py (for PDFs), python-docx (for DOCX), python-pptx (for PPT).
- **Reintegration**: Convert to clean formats like markdown, HTML, or CSV.
- **Post-Processing**: Reinsert tables into the consolidated document.

#### 2.3 Images
- **Extraction**: Use Pillow, PyMuPDF, python-docx, python-pptx.
- **OCR**: Use Tesseract/Google Vision API for extracting text from images.
- **Reintegration**: Insert image references into the consolidated document.

### 3. General Preprocessing Pipeline

1. **Text Extraction**: Extract raw text and handle structure.
2. **Image/Diagram Processing**: Extract and process non-text content.
3. **Table Handling**: Extract and process tables into structured formats.
4. **Formatting and Clean-Up**: Normalize text and remove non-informative elements.
5. **Annotation**: Annotate references for diagrams, tables, and images.

### 4. Merging Content from Multiple Files

1. **Combine Text**: Merge text while retaining structure.
2. **Redundancy Removal**: Use sentence embeddings (e.g., SBERT) to remove duplicates.
3. **Summarization**: Use summarization models (e.g., BERT, T5) to condense content.
4. **Reintegration**: Reinsert annotated references for images, diagrams, and tables.

## Technologies Used

- **Python Libraries**:
  - PyPDF2, pdfplumber, PyMuPDF for PDFs
  - python-docx for DOCX
  - python-pptx for PPT
  - camelot, tabula-py for table extraction
  - Tesseract for OCR
  - Flask for backend
  - SBERT for redundancy removal
  - BERT, T5 for summarization
- **Deployment**:
  - Docker
  - Vercel for hosting
- **Tools**:
  - Git for version control

## How to Use

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
