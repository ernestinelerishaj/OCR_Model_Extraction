import cv2
import numpy as np
import matplotlib.pyplot as plt
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# Image Preprocessing Function
def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply binary thresholding to highlight text
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # (Optional) Dilate to make text regions more prominent
    kernel = np.ones((2,2), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    
    # (Optional) Apply morphological transformation for better OCR readability
    morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    morph = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, morph_kernel)
    
    return morph

# OCR extraction and header detection function
def extract_header_fields(image_path):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)
    
    # Save the preprocessed image for reference
    cv2.imwrite('preprocessed_image.png', preprocessed_image)

    # Load doctr OCR model
    ocr_model = ocr_predictor(pretrained=True)

    # Perform OCR on the preprocessed image
    doc = DocumentFile.from_images('preprocessed_image.png')
    result = ocr_model(doc)

    # Extract the first page (assuming single page table)
    page = result.pages[0]

    # Parse the words and their bounding boxes
    words = [word.value for block in page.blocks for line in block.lines for word in line.words]
    boxes = [word.geometry for block in page.blocks for line in block.lines for word in line.words]

    # Convert boxes to a more usable format (x_min, y_min, x_max, y_max) in relative coordinates
    boxes = np.array([[(box[0][0], box[0][1]), (box[1][0], box[1][1])] for box in boxes])

    # Extract words and boxes from the top 15% of the image (header region)
    header_cutoff = 0.15  # Adjust as needed
    header_indices = [i for i, box in enumerate(boxes) if box[0][1] < header_cutoff]

    # Extract words and boxes from the header area
    header_words = [words[i] for i in header_indices]
    header_boxes = [boxes[i] for i in header_indices]

    return header_words, header_boxes, preprocessed_image

# Function to display the preprocessed image and extracted header fields
def display_results(image_path):
    header_fields, header_boxes, preprocessed_image = extract_header_fields(image_path)
    
    # Display the preprocessed image
    plt.figure(figsize=(10, 10))
    plt.imshow(preprocessed_image, cmap='gray')
    plt.title('Preprocessed Image')
    plt.axis('off')
    plt.show()

    # Print the extracted header fields and their positions
    print("Extracted Header Fields with Bounding Boxes:")
    for word, box in zip(header_fields, header_boxes):
        print(f"Field: '{word}', Bounding Box: {box}")

# Example usage
image_path = "tables\Table_2.jpg"  # Replace with your image file path
display_results(image_path)
