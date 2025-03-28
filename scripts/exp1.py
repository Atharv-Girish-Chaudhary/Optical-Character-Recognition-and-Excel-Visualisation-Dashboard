import json
import os
import cv2
import numpy as np
import pytesseract
import pandas as pd

import modules.ROI as ROI

dict_format = {}

#Assisgning Directories
outputs_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Outputs")
images_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Testing Images")
os.chdir(images_directory)


def Table_conv(image) -> None:
    """Loading an image and performing binarization and inversion to the image"""
    image = ROI.roi(image)
    cv2.imwrite(os.path.join(os.path.join(os.getcwd(), 'Debugging_TableText'), 'roi_image.jpg'), image)
    base_image = image.copy()
    image_binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY, cv2.THRESH_OTSU)[1]
    image_binary_inv = cv2.bitwise_not(image_binary)
    """Finding the overall length of Kernel using Numpy Array and Using that length to create horizontal kernel with 
    width equal to one pixel and height equal to kernel length and vertical 
    kernels having width equal to kernel length and height of one pixel"""
    kernel_len = np.array(image).shape[1] // 100  # Taking 100th of the original pixel length
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))  # To be used for further image preprocessing

    """Vertical line detection and Horizontal line detection"""
    image_v = cv2.erode(image_binary_inv, vertical_kernel, iterations=3)
    vertical_lines = cv2.dilate(image_v, vertical_kernel, iterations=3)
    image_h = cv2.erode(image_binary_inv, horizontal_kernel, iterations=3)
    horizontal_lines = cv2.dilate(image_h, horizontal_kernel, iterations=3)

    # Debugging :
    # cv2.imwrite(os.path.join(os.path.join(os.getcwd(), 'Debugging_TableText'), 'vertical_eroded_image.jpg'), image_v)
    # cv2.imwrite(os.path.join(os.path.join(os.getcwd(), 'Debugging_TableText'), 'vertical_lines.jpg'), vertical_lines)
    # cv2.imwrite(os.path.join(os.path.join(os.getcwd(), 'Debugging_TableText'), 'horizontal_eroded_image.jpg'), image_h)
    # cv2.imwrite(os.path.join(os.path.join(os.getcwd(), 'Debugging_TableText'), 'horizontal_lines.jpg'), horizontal_lines)

    """Combining Vertical and Horizontal Lines assuming they have same weights"""
    image_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0)

    # Debugging :
    # cv2.imwrite(os.path.join(os.path.join(os.getcwd(), 'Debugging_TableText'), 'lines.jpg'), image_vh)

    """Finding contours"""
    image_vh = cv2.cvtColor(image_vh, cv2.COLOR_BGR2GRAY)
    cnts = cv2.findContours(image_vh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # Change this accordingly
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=lambda y: cv2.boundingRect(y)[1])

    x_coord = []
    y_coord = []
    unique_x = []
    unique_y = []
    rec = {}  # x coordinates : widths and heights
    coord = []
    max_width_height = []

    # Assigning values in above lists
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        x_coord.append(x)
        y_coord.append(y)
        coord.append([x, y, w, h])

    x_coord = sorted(x_coord)
    y_coord = sorted(y_coord)

    # Adding elements to the dictionary of x
    for c in range(0, len(coord)):
        x = coord[c][0]
        if x not in rec:
            rec[x] = []
        rec[x].append([coord[c][2], coord[c][3]])

    # Finding the unique x coordinate
    for i in x_coord:
        if i in unique_x:
            pass
        elif x_coord.count(i) >= 1:
            unique_x.append(i)

    for i in y_coord:
        if i in unique_y:
            pass
        elif y_coord.count(i) >= 1:
            unique_y.append(i)

    # Finding max height and width
    for x in unique_x:
        mw, mh = [], []
        for r in rec[x]:
            mw.append(r[0])
            mh.append(r[1])
        max_width = max(mw)
        max_height = max(mh)
        max_width_height.append((max_width, max_height))

    columns = len(unique_x) - 1
    rows = len(unique_y) - 1
    unique_x.append(image.shape[1])

    """Extracting each column present in the table and performing OCR to get desired text output"""
    for column_no in range(1, len(unique_x) - 1):
        x = unique_x[column_no]
        y = unique_y[0]
        x2 = unique_x[column_no + 1]
        y2 = max_width_height[0][1]
        # cv2.rectangle(image, (x, y), (x2, y2), (0, 0, 255), 3)
        extracted_image = base_image[y:y2, x:x2]
        ocr_converion(extracted_image)  # call tesseract conversion taking extracted_image as input

        # Debugging :
        # cv2.imwrite(os.path.join(os.path.join(os.getcwd(), 'Debugging_TableText'), f'extracted_lines_{column_no}.jpg'),
        #             extracted_image)


def ocr_converion(extracted_image):
    result = pytesseract.image_to_string(extracted_image)
    result.lstrip()
    column_data_list = result.split("\n")
    column_data_list = [val for val in column_data_list if val]
    if column_data_list:
        header = column_data_list[0]
        data = column_data_list[1::]
        dict_format[header] = data


def display_table():
    # pass
    df = pd.DataFrame(dict_format)
    print(df.to_string(index=False, justify='left'))



if __name__ == "__main__":
    path = '2.jpg'
    image = cv2.imread(path)
    Table_conv(image)
    data = json.dumps(dict_format, indent=4)
    print(data)
    # display_table()
