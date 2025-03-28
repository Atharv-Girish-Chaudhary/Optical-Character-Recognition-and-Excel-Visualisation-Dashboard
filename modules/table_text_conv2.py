import cv2
import pytesseract
import os
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

dict_format = {}

def preprocess_image(image):
    """Preprocess image for table extraction."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inv = cv2.bitwise_not(gray)
    _, thresh = cv2.threshold(inv, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return thresh

def extract_lines(thresh):
    """Extract horizontal and vertical lines using morphological operations."""
    kernel_length = max(10, np.array(thresh).shape[1] // 150)
    
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))

    horizontal_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

    final_table = cv2.addWeighted(horizontal_lines, 0.5, vertical_lines, 0.5, 0.0)
    return final_table

def ocr_worker(cell_img):
    """Perform OCR on a single cell image."""
    custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,.'
    return pytesseract.image_to_string(cell_img, config=custom_config).strip()

def extract_cells(image, final_table):
    """Extract cells using contours and apply OCR in parallel."""
    contours, _ = cv2.findContours(final_table, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])

    extracted_data = []
    cell_images = []
    coords = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 10 and h > 10:  # Ignore small contours
            cell_img = image[y:y+h, x:x+w]
            cell_images.append(cell_img)
            coords.append((x, y, w, h))

    # Perform OCR using multithreading
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(ocr_worker, cell_images))

    for (x, y, w, h), text in zip(coords, results):
        extracted_data.append((x, y, w, h, text))

    return extracted_data

def convert_table(image_path):
    """Main function to process image and extract table data."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to read image at {image_path}")
        return

    # Resize for faster processing if image is large
    # if max(image.shape[:2]) > 1000:
    #     image = cv2.resize(image, (1000, 1000))

    thresh = preprocess_image(image)
    final_table = extract_lines(thresh)
    extracted_data = extract_cells(image, final_table)

    # Organize data into a dataframe
    if extracted_data:
        df_data = sorted(extracted_data, key=lambda x: (x[1], x[0]))
        data = [item[4] for item in df_data]
        dict_format['Extracted Data'] = data
        df = pd.DataFrame(dict_format)
        output_path = r'data\output\Extracted_Table.csv'
        df.to_csv(output_path, index=False)
        print(f"Table data saved to {output_path}")
    else:
        print("No table data extracted.")

if __name__ == '__main__':
    image_path = r"data\processed\Final Test\Final Test_page_1.png"
    convert_table(image_path)
