from PIL import Image, ImageEnhance, ImageFilter  # For image preprocessing
import pytesseract  # For OCR

# Set the path to the Tesseract executable (update path if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Change to your tesseract.exe path

def preprocess_image(image_path):
    """
    Preprocess the image to improve OCR accuracy:
    - Converts the image to grayscale.
    - Enhances sharpness.
    - Reduces noise using a filter.
    """
    image = Image.open(image_path)  # Load image
    image = image.convert("L")  # Convert to grayscale
    image = image.filter(ImageFilter.MedianFilter(size=3))  # Apply a median filter to remove noise
    enhancer = ImageEnhance.Contrast(image)  # Enhance contrast
    image = enhancer.enhance(2)  # Increase contrast by a factor of 2
    return image

def extract_text(image_path):
    """
    Extract text from the given image.
    """
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)

    # Extract text using Tesseract OCR
    config = "--psm 6"  # Configure for OCR (modify if necessary)
    extracted_text = pytesseract.image_to_string(preprocessed_image, config=config)

    # Add the extracted text as a single element in a list
    text_list = [extracted_text]

    return text_list

def main():
    # Provide the path to your image
    image_path = r"C:\Users\Kruttika\OneDrive\Desktop\Screenshot 2025-01-26 223226.png"  # Replace with your image file path

    # Extract text from the image
    extracted_text_list = extract_text(image_path)

    # Print the extracted text in a list format
    print("Extracted Text as a List:")
    print(extracted_text_list)

if __name__ == "__main__":
    main()

