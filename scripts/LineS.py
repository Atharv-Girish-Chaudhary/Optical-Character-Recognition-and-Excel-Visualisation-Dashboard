import cv2
import numpy as np
import os
import csv
import pytesseract
import pandas as pd

outputs_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Outputs")
images_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Testing Images")

os.chdir(images_directory)


# Load the table image
img = cv2.imread('7.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding to preprocess the image
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 2)

# Use pytesseract to extract the text from the image
data = pytesseract.image_to_string(thresh)

# Split the extracted text into rows and columns
rows = data.split('\n')
cols = rows[0].split()

# Create a pandas dataframe from the extracted rows and columns
df = pd.DataFrame(columns=cols)

for row in rows[1:]:
    df = df.append(pd.Series(row.split(), index=cols), ignore_index=True)

# Save the dataframe as a CSV file
df.to_csv('table_data.csv', index=False)

