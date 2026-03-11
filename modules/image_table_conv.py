import pytesseract
import os
import sys
import numpy as np

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import modules.table_text_conv2 as table_text_conv2
    import pdf2image
    from modules import directories
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None

except ImportError as e:
    print(f"Import Error: {e}. Please ensure all dependencies are installed.")
    sys.exit(1)

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def iterate_files(root_input_dir=r'data\raw', root_output_dir=r'data\processed'):
    """Iterates through PDF files stored in the root input directory and processes them."""
    try:
        directories.create_root_folder_dir([root_input_dir, root_output_dir])
        
        for entry in os.scandir(os.path.join(os.getcwd(), root_input_dir)):
            if entry.is_file() and entry.name.endswith('.pdf'):
                pdf_name = os.path.splitext(os.path.basename(entry.path))[0]
                sub_folder_dir = directories.create_sub_folder_dir(root_output_dir, pdf_name)
                convert_bytes(pdf_name, entry.path, sub_folder_dir)
    except Exception as e:
        print(f"Failed to iterate through files: {e}")

def convert_bytes(pdf_name, pdf_path, sub_folder_dir):
    """Converts PDF into images, saves images as PNG, and performs OCR."""
    try:
        pages = pdf2image.convert_from_path(pdf_path, 400)
        
        for page_no, page in enumerate(pages):
            # Convert to PNG and save
            image = page.convert("RGB")
            file_name = f"{pdf_name}_page_{page_no + 1}.png"
            image_path = os.path.join(sub_folder_dir, file_name)
            image.save(image_path, "PNG")

            print(f"Saved image: {image_path}")
            
            # Perform OCR
            numpy_image = np.array(image)
            table_text_conv2.convert_table(numpy_image)
            convert_text(numpy_image, sub_folder_dir, pdf_name, page_no + 1)

            # Free memory
            image.close()
    except Exception as e:
        print(f"Failed to convert PDF to images: {e}")

def convert_text(image, sub_folder_dir, img_name, page_no):
    """Performs OCR on an image and saves the result to a text file."""
    try:
        result = pytesseract.image_to_string(image)
        file_path = os.path.join(sub_folder_dir, f"{img_name}_page_{page_no}.txt")
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(result)
        print(f"OCR result saved to {file_path}")
    except Exception as e:
        print(f"Error performing OCR on {img_name}_page_{page_no}: {e}")

if __name__ == "__main__":
    iterate_files()
