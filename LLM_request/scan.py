#add to reqs
# !pip install paddlepaddle paddleocr 

#Import necessary libraries
from paddleocr import PaddleOCR, draw_ocr
import matplotlib.pyplot as plt
from PIL import Image
import requests
import os # Import os to check if font path exists later if needed (optional)
import sys

#img_pth = "fanta.jpg" # Using png as original source hints it might be better


###################################################################################################
def scan_text(image_path):
    ocr = PaddleOCR(use_angle_cls=False, lang='pt', show_log=False)
    # Step 5: Perform OCR on the image
    # Check if the image file exists before processing
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        exit()

    try:
        result = ocr.ocr(image_path, cls=False)
    except Exception as e:
        print(f"Error during OCR processing: {e}")
        exit() # Exit if OCR fails


    # Step 6: Extract and display text
    print("--- Detected Text ---")
    # Ensure result[0] is not None before iterating
    if result and result[0]:
        for idx, line in enumerate(result[0]):
            # Basic check for line structure
            if len(line) == 2 and isinstance(line[1], (list, tuple)) and len(line[1]) == 2:
                print(f"Line {idx+1}: Text: {line[1][0]} (Confidence: {line[1][1]:.4f})")
            else:
                print(f"Line {idx+1}: Unexpected format: {line}")
    else:
        print("No text detected or result format is unexpected.")
    print("---------------------")


    # Step 7: Visualize the results
    # Load the image using PIL
    try:
        image = Image.open(image_path).convert('RGB')
    except Exception as e:
        print(f"Error opening image for visualization: {e}")
        exit()

    # Extract boxes, texts, and scores (handle potential None result)
    boxes = [line[0] for line in result[0]] if result and result[0] else []
    texts = [line[1][0] for line in result[0]] if result and result[0] else []
    scores = [line[1][1] for line in result[0]] if result and result[0] else []
    return texts

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_test = os.path.join(base_dir, "fanta.jpg")
    print(scan_text(path_test))