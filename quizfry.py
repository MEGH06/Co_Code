import re
import os
import PyPDF2
import google.generativeai as genai

genai.configure(api_key="AIzaSyDo3kfhSuAoV-O4SfZ_LJc0BRdTc2EFx9o")

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""

def query_gemini_api(document_text, user_query):
    prompt = f"Based on the following document:\n\n{document_text}\n\n{user_query}"
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return response.text if response else "No response from Gemini."

def parse_mcq_output(mcq_text):
    question_pattern = re.findall(r"(\d+)\.\s(.*?)\n\s*a\)\s(.*?)\n\s*b\)\s(.*?)\n\s*c\)\s(.*?)\n\s*d\)\s(.*?)\n",mcq_text,re.DOTALL)

    questions_dict = {
        num: {
            "question": question.strip(),
            "options": {
                "a": option_a.strip(),
                "b": option_b.strip(),
                "c": option_c.strip(),
                "d": option_d.strip()
            }
        }
        for num, question, option_a, option_b, option_c, option_d in question_pattern
    }

    answer_pattern = re.search(r"\{(.*?)\}", mcq_text, re.DOTALL)
    answers_dict = {}
    if answer_pattern:
        answer_text = answer_pattern.group(1)
        answer_entries = re.findall(r'"(\d+)":\s*"([a-d])"', answer_text)
        answers_dict = {num: ans for num, ans in answer_entries}

    return questions_dict, answers_dict

def chatbot():
    file_path = r"C:\Users\Megh\Desktop\sample\sample.pdf"  # Replace with your actual PDF file path
    
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        print("Error: File not found.")
        return
    
    print("Processing.....\nYour quizzard will be live any moment")

    document_text = extract_text_from_pdf(file_path)
    
    if not document_text:
        print("Error: No text extracted from the document.")
        return

    print("\nDocument processed. Generating MCQs...")
    
    user_query = ("Based on the following document:\n\n"
                  f"{document_text}\n\n"
                  "Generate 10 multiple-choice questions (MCQs) from this document. \n\n"
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
                  "...(repeat for 10 questions)\n\n"
                  "### Answers:\n"
                  "{ \"1\": \"b\", \"2\": \"d\", \"3\": \"a\", ..., \"10\": \"c\" }\n\n"
                  "Ensure that:\n"
                  "- Each question has 4 answer choices labeled (a, b, c, d).\n"
                  "- The correct answer should be provided in a JSON dictionary format separately.\n"
                  "- Do not add extra text, explanations, or formatting beyond the requested structure.\n\n"
                  "Return only the questions and answers in the specified format.")

    mcq_output = query_gemini_api(document_text, user_query)

    questions, answers = parse_mcq_output(mcq_output)

    print("\nExtracted Questions Dictionary:\n", questions)
    print("\nExtracted Answers Dictionary:\n", answers)

if __name__ == "__main__":
    chatbot()
