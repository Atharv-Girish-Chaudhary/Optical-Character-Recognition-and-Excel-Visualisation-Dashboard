#________________________________________________________________________DASHBOARD VISUALIZATION___________________________________________________________________________________________________#

#IMPORTING REQUIRED MODULES:
import cv2
import pytesseract
import os
import modules.ROI as ROI
import numpy as np
import pandas as pd
import json

# OPTIONAL:
# outputs_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Outputs")
# images_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Testing Images")
# os.chdir(images_directory)

dict_format = {}

# CODE:
def convert_table(image) -> None:
    '''This function extracts the table from the image and performs ocr on it.
       @Parameter: image
       @return: None
    '''
    #Reading the image and applying Basic Preprocessing
    image=ROI.roi(image)                                                      #Reads and extracts the region of interest from the image.
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
    # cv2.imwrite(os.path.join(outputs_directory,"final.jpg"),final_table)    #For debugging purposes.
    cnts=cv2.findContours(final_table,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE) #Finds the contours in the image.
    cnts=cnts[0] if len(cnts)==2 else cnts[1]                                 #In this context, the contour is the path or the edge.
    cnts=sorted(cnts,key=lambda y:cv2.boundingRect(y)[1])

    #Declaring lists and variables
    xcoords=[]
    ycoords=[]
    heights=[]
    unique_x=[]
    unique_y=[]
    rec={}
    coords=[]
    max_width=[]
    max_height=0

    #Drawing the contours
    for c in cnts:                         
        x,y,w,h=cv2.boundingRect(c)
        xcoords.append(x)
        ycoords.append(y)
        coords.append([x,y,w,h])
        heights.append(h)

    xcoords=sorted(xcoords)
    ycoords=sorted(ycoords)

    #Adding elements to the dictionary of 'x' 
    '''Explaination of rec: Stores all the related width and heights of bounding boxes 
       originating from that 'x' coordinate.'''

    for c in coords:                                    #'c' in this context, are the coordinates of the bounding box.
        x = c[0]                                        #This chooses the x coordinate from that bouding box 'c'.
        if x not in rec:
            rec[x]=[[c[2],c[3]]]                        #Chooses the width and height from that bouding box 'c'.
        else:
            rec[x].append([c[2],c[3]])
    
    # Finding the unique x coordinate 
    for i in xcoords:
        if(i in unique_x):
            pass
        elif(xcoords.count(i)>=1):
            unique_x.append(i)

    #Finding the unique y coordinate 
    for i in ycoords:
        if(i in unique_y):
            pass
        elif(ycoords.count(i)>=1):
            unique_y.append(i)

    #Finding max width for the x_coordinate
    for x in unique_x:
        mw,mh=[],[]
        for r in rec[x]:    
            mw.append(r[0])  
        max_width.append(max(mw))

    #Calculating the values of no of columns and rows and max_height
    columns=len(unique_x)-1
    rows=len(unique_y)-1
    max_height=max(heights)

    for i in range(1,len(unique_x)-1):
        x=unique_x[i]
        y=unique_y[0]
        x1=unique_x[i]+max_width[i]
        y1=max_height
        cv2.rectangle(image,(unique_x[i],unique_y[0]),(unique_x[i]+max_width[i],unique_y[0]+max_height),[0,0,255],2)
        extracted_image=base_image[y:y1,x:x1]
        result = pytesseract.image_to_string(extracted_image)
        print(result)
        #Debug:
        # cv2.imwrite(os.path.join(outputs_directory,"extracted"+f"{i}"+".jpg"),extracted_image)
        # ocr_converion(extracted_image)                  #Call the ocr_conversion function to convert the given image to text. 

    #Debugging:

    # cv2.imwrite(os.path.join(outputs_directory,"ContourMethod.jpg"),image)

def ocr_converion(image) -> None:
    '''This function converts the image into a Dictionary. 
       @Parameter: image
       @return: None'''
    result = pytesseract.image_to_string(image)
    result.lstrip()
    column_data_list = result.split("/n")
    column_data_list = [val for val in column_data_list if val]
    if column_data_list:
        header = column_data_list[0]
        data = column_data_list[1::]
        dict_format[header] = data

def display_table() -> None:
    '''This function displays the table.
       @Parameter: None
       @return: None'''
    # pass
    df = pd.DataFrame(dict_format)
    print(df.to_string(index=False, justify='left'))

if __name__=='__main__':
    path = 'C:/Users/anike/OneDrive/Desktop/Mini Project Sem IV/mini-project/OCR/Testing Images/3.jpg'
    image = cv2.imread(path)
    convert_table(image)
    data = json.dumps(dict_format, indent=4)
    print(data)
    # display_table()