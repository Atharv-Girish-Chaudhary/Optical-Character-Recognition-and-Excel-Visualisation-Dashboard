import cv2
import os

def roi(image):
    """
    Extracts ROI (region of interest) using bounding boxes.

    Parameters:
    - image (numpy.ndarray): Input image.

    Returns:
    - numpy.ndarray: Extracted ROI or original image if extraction fails.
    """
    base_image = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inv = cv2.bitwise_not(gray)
    thresh = cv2.threshold(inv, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))  
    dilate = cv2.dilate(thresh, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(dilate, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("No contours found. Returning original image.")
        return base_image

    # Extract largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    if w < 10 or h < 10:
        print("Extracted region too small. Returning original image.")
        return base_image

    roi = base_image[y:y+h, x:x+w]
    return roi

def ensure_directory(path):
    """Ensure the directory exists."""
    os.makedirs(path, exist_ok=True)

if __name__ == '__main__':
    base_dir = os.path.join(os.getcwd(), "OCR")
    outputs_directory = os.path.join(base_dir, "Outputs")
    images_directory = os.path.join(base_dir, "Testing Images")

    ensure_directory(outputs_directory)

    image_path = os.path.join(images_directory, "trial1.png")
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Failed to read image from {image_path}")
    else:
        roi_image = roi(image)
        output_path = os.path.join(outputs_directory, 'roi.jpg')
        cv2.imwrite(output_path, roi_image)
        print(f"ROI saved to {output_path}")
