import os
import cv2
import numpy as np
import modules.ROI as ROI

#Assisgning Directories
outputs_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Outputs")
images_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Testing Images")
os.chdir(images_directory)


#Reading and doing basic image Preprocessing
image=cv2.imread("8.jpg") #-> put the name of the image here
image=ROI.roi(image)
base_image=image.copy()
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
threshAbs=cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,3,15)
inv=cv2.bitwise_not(threshAbs)


#Drawing Line Function
def drawLines(lines):
    for line in lines:
        x1,y1,x2,y2=line[0]
        cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)


#Horizontal Line Detection and Drawing
horizontalStructure=cv2.getStructuringElement(cv2.MORPH_RECT,(15,1))
horizontal=cv2.erode(inv,horizontalStructure,1)
# horizontal = cv2.dilate(horizontal,horizontalStructure)
# horizontal = cv2.dilate(horizontal, (1,1), iterations=5)
# horizontal = cv2.erode(horizontal, (1,1), iterations=5)
canny=cv2.Canny(horizontal,100,255)
cv2.imwrite(os.path.join(outputs_directory,"CannyH.png"),canny)
linesH=cv2.HoughLinesP(canny,1,np.pi/180,100)
drawLines(linesH)


#Vertical Line Detection and Drawing
verticalStructure=cv2.getStructuringElement(cv2.MORPH_RECT,(1,15))  
vertical=cv2.erode(inv,verticalStructure,1)
# vertical = cv2.dilate(vertical,verticalStructure)
# vertical = cv2.dilate(vertical, (1,1), iterations=8)
# vertical = cv2.erode(vertical, (1,1), iterations=7)
canny=cv2.Canny(vertical,100,255)
cv2.imwrite(os.path.join(outputs_directory,"CannyV.png"),canny)
linesV=cv2.HoughLinesP(canny,1,np.pi/180,100)
drawLines(linesV)


# #Writing The Detected Lines Image
cv2.imwrite(os.path.join(outputs_directory,"LineDetection.png"),image)

