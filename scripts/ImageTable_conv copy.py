from PIL import Image
from  Modules import Directories 
import pdf2image
import pytesseract
import io
import os
import modules.table_text_conv2 as table_text_conv2
import cv2
import numpy as np


def iterate_files(root_input_dir: str, root_output_dir: str) -> None:
    """ This functions iterates through the pdf files stored in root input directory and creates a sub folder with
    pdf file extension as its name and stores the sub folder created in root output directory """

    try:
        Directories.create_root_folder_dir([root_input_dir, root_output_dir])
        for entry in os.scandir(os.path.join(os.getcwd(), root_input_dir)):
            if entry.is_file() and entry.name.endswith('.pdf'):
                pdf_name = os.path.splitext(os.path.basename(entry.path))[0]
                sub_folder_dir = Directories.create_sub_folder_dir(root_output_dir, pdf_name)
                convert_bytes(pdf_name, entry.path, sub_folder_dir)
    except OSError as e:
        raise Exception(f"Failed to iterate through files : {e}")


def convert_bytes(pdf_name: str, pdf_path: str, sub_folder_dir: str) -> None:
    """ This function converts pdf into PIL images , each image_pg-no is then saved as JPEG image to  BytesIO object.
    The BytesIO object is then used to load the image data into a Pillow Image object,
    which is sent to OCR conversion function """

    try:
        pages = pdf2image.convert_from_path(pdf_path, 400)
        for page_no, page in enumerate(pages):
            jpeg_bytes = io.BytesIO()
            page.save(jpeg_bytes, format="JPEG")
            jpeg_bytes.seek(0)
            image = Image.open(jpeg_bytes)
            numpy_image = np.array(image)
            # Add ".jpg" file extension to the file name
            # file_name = f"/Users/keegz_dsouza/Documents/Excel Dashboard Visualization/mini-project/test_{page_no}.jpg"
            # cv2.imwrite(file_name, numpy_image)
            # Make a copy of the numpy array to avoid modifying the original
            numpy_image_copy = numpy_image.copy()
            table_text_conv2.convert_table(numpy_image_copy)

    except Exception as e:
        raise RuntimeError(f"Failed to create images : {e}")


def convert_text(image, sub_folder_dir, img_name, page_no):
    result = pytesseract.image_to_string(image)
    file = open(os.path.join(sub_folder_dir, f"{os.path.splitext(f'{img_name}_{page_no}')[0]}" + ".txt"), 'w')
    file.write(result)
    file.close()


if __name__ == "__main__":
    root_input_dir = 'Files'
    root_output_dir = 'Files'
    iterate_files(root_input_dir, root_output_dir)
