import os
import cv2
import numpy as np
import modules.ROI as ROI
import pytesseract

def linedetector(image):
    '''This function detects and draws The Column Line Segments on the given output_image
       @parameter: Image
       @return : output_image,List of lines'''

    image=ROI.roi(image)
    output_image=image.copy()
    gray=cv2.cvtColor(output_image,cv2.COLOR_BGR2GRAY)
    # inv=cv2.bitwise_not(gray)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    
    # cv2.imwrite(os.path.join(outputs_directory,"blur.jpg"),blur) #------------------------------------> Use this for Debugging.
    # threshAbs=cv2.adaptiveThreshold(blur,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU,3,15)
    thresh=cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1] #-------------------------> This is used
    # cv2.imwrite(os.path.join(outputs_directory,"threshedInverse.jpg"),thresh)  #----------------------> Use this for Debugging.
    #Drawing Line Function
    def drawLines(lines):
        for line in lines:
            x1,y1,x2,y2=line[0]
            cv2.line(output_image,(x1,y1),(x2,y2),(0,255,0),2)


    # Vertical Line Detection and Drawing
    verticalStructure=cv2.getStructuringElement(cv2.MORPH_RECT,(1,15))  
    horVert=cv2.getStructuringElement(cv2.MORPH_RECT,(15,1))
    vertical = cv2.dilate(thresh,horVert,1)
    vertical=cv2.erode(vertical,verticalStructure,1)
    # vertical = cv2.dilate(vertical, (1,1), iterations=1)
    vertical = cv2.erode(vertical,verticalStructure, iterations=2)
    vertical = cv2.erode(vertical,horVert, iterations=1)
    # cv2.imwrite(os.path.join(outputs_directory,"DilatedVertical.jpg"),vertical)  #---------------------> Use for debugging
    
    #Edge Detection
    canny=cv2.Canny(vertical,75,255)
    # cv2.imwrite(os.path.join(outputs_directory,"CannyV.png"),canny) #----------------------------------> Use for debugging
    
    linesV=cv2.HoughLinesP(vertical,1,np.pi/180,100)
    drawLines(linesV)
    return output_image,linesV

if __name__=="__main__":

    outputs_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Outputs")
    images_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Testing Images")
    os.chdir(images_directory)
    image=cv2.imread("3.jpg")
    otp,ln=linedetector(image)
    cv2.imshow("otp",otp)
    cv2.waitKey(0)
    result=pytesseract.image_to_string(otp)
    print(result)
