#IMPORTING REQUIRED MODULES:

import cv2
import pytesseract
import os
import modules.ROI as ROI
import numpy as np
import pandas as pd
import json
from pytesseract import Output

# OPTIONAL:
print(os.getcwd())
outputs_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Outputs")
images_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Testing Images")
os.chdir(images_directory)

#Declaring Global Variables 
columns={}

# CODE:
def convert_table(image) -> None:
    '''This function extracts the table from the image and performs ocr on it.
       @Parameter: image
       @return: None
    '''
    #Reading the image and applying Basic Preprocessing
    image=ROI.roi(image)                                                      #Maintainance   
    cv2.imwrite(os.path.join(outputs_directory,'roi.jpg'),image)              #Maintainance                                                          
                                                                              #Reads and extracts the region of interest from the image.
    base_image=image.copy()                                                   #Copies the image to another image called as Base Image.
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)                               #Converts the image to grayscale.
    inv=cv2.bitwise_not(gray)                                                 #Inverts the colour of the image.
    thresh=cv2.threshold(inv,100,255,cv2.THRESH_BINARY,cv2.THRESH_OTSU)[1]    #Applies thresholding to the image.

    # Horizontal Lines
    kernel_length=np.array(thresh).shape[1]//100                              #Kernel length is the area on which the operation is to be performed '(1/100)th size of the image'.
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_length,1))
    openedH=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=3)       #Applies morphological image preprocessing on the image.

    #Vertical Lines
    kernel_length=np.array(thresh).shape[1]//100
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(1,kernel_length))
    openedV=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=3)

    #Getting Final Image
    final_table=cv2.addWeighted(openedV,1, openedH, 1, 0.0)
    cv2.imwrite(os.path.join(outputs_directory,"final.jpg"),final_table)    #For debugging purposes.
    cnts=cv2.findContours(final_table,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE) #Finds the contours in the image.
    cnts=cnts[0] if len(cnts)==2 else cnts[1]                                 #In this context, the contour is the path or the edge.
    cnts=sorted(cnts,key=lambda y:cv2.boundingRect(y)[1]) 
    #Declaring lists and variables

    coords=[]
    temp=None

    #Drawing the contours
    for c in cnts:                         
        x,y,w,h=cv2.boundingRect(c)
        coords.append([x,y,w,h])

    coords = sorted(coords, key=lambda x: x[0])
    hmin=0

    for c in coords:
        x,y,w,h=c
        if(hmin==0):
            hmin=h
        elif(h<hmin):
            hmin=h
    print(hmin)
    for c in coords:
        x,y,w,h=c
        cv2.rectangle(image,(x,y),(x+w,y+h),[0,0,255],2)
        extracted_image=base_image[y:y+h,x:x+w]
        cv2.imwrite(os.path.join(outputs_directory,'extract.jpg'),extracted_image)
        # result=pytesseract.image_to_data(extracted_image,config='--psm 11',output_type=Output.DICT)
        result=pytesseract.image_to_string(extracted_image)
        # print(result)
        result=result.replace("\n","")
        if result=="":
            result="Null Value \n"
        if(h<=hmin):    
            columns[result]=[]
            temp=result
            continue        
        if temp:
            columns[temp].append(result)  
        
        # file=open("result.txt",'a')
        # file.write(columns)

        #Debugging:
        # cv2.imwrite(os.path.join(outputs_directory,"extracted"+f"{i}"+".jpg"),extracted_image)
        # i+=1

    #Debugging:
    # cv2.imwrite(os.path.join(outputs_directory,"ContourMethod.jpg"),image)


def display_table() -> None:
    """This function displays the table.
       @Parameter: None
       @return: None"""
    # pass
    data = json.dumps(columns, indent=4)
    print(data)

if __name__=='__main__':
    path = 'trial1.png'
    image = cv2.imread(path)
    convert_table(image)
    display_table()
