
import os
import pytesseract
from PIL import Image
# OPTIONAL:
outputs_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Outputs")
images_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Testing Images")
os.chdir(images_directory)

image=Image.open(os.path.join(outputs_directory,"extracted1.jpg"))
result=pytesseract.image_to_string(image)
print(result)