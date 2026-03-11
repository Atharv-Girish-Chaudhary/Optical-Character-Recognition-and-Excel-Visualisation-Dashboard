#Useless Attempt
import cv2
import pytesseract
import os
import modules.ROI as ROI
import numpy as np

outputs_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Outputs")
images_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Testing Images")
os.chdir(images_directory)
#hint:no. of contours

image=cv2.imread("2.jpg")
output_image=image.copy()
image=ROI.roi(image)
base_image=image.copy()

gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
inv=cv2.bitwise_not(gray)
# thresh=cv2.adaptiveThreshold(inv,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,15)
thresh=cv2.threshold(inv,100,255,cv2.THRESH_BINARY,cv2.THRESH_OTSU)[1]


# Horizontal Lines
kernel_length=np.array(thresh).shape[1]//100
kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_length,1))
openedH=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=3)

#Vertical Lines
kernel_length=np.array(thresh).shape[1]//100
kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(1,kernel_length))
openedV=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=3)

#Getting Final Image
final_table=cv2.addWeighted(openedV,0.5, openedH, 0.5, 0.0)
t=cv2.threshold(final_table,100,255,cv2.THRESH_BINARY,cv2.THRESH_OTSU)[1]

cv2.imwrite(os.path.join(outputs_directory,"final.jpg"),final_table)

cnts=cv2.findContours(final_table,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE) #Change this accordingly
cnts=cnts[0] if len(cnts)==2 else cnts[1]
cnts=sorted(cnts,key=lambda x:cv2.boundingRect(x)[1])

#start from here
xcoords=[]
ycoords=[]
uniquex=[]
uniquey=[]
rec={}
coords=[]
max_width_height=[]

#Drawing the contours
for c in cnts:                         
    x,y,w,h=cv2.boundingRect(c)
    xcoords.append(x)
    ycoords.append(y)
    coords.append([x,y,w,h])
    

xcoords=sorted(xcoords)
ycoords=sorted(ycoords)
#Adding elements to the dictionary of x 
for c in range(0,len(coords)):
    x = coords[c][0]
    if x not in rec:
        rec[x] = []
    rec[x].append([coords[c][2],coords[c][3]])   #Error is  here
#Finding the unique x coordinate 
for i in xcoords:
    if(i in uniquex):
        pass
    elif(xcoords.count(i)>=1):
        uniquex.append(i)

for i in ycoords:
    if(i in uniquey):
        pass
    elif(ycoords.count(i)>=1):
        uniquey.append(i)

#Finding max height and width
for x in uniquex:
    mw,mh=[],[]
    for r in rec[x]:    
        mw.append(r[0])  #error is here
        mh.append(r[1])
    max_width=max(mw)
    max_height=max(mh)
    max_width_height.append((max_width,max_height))

# print(rec)

# print(max_width_height) #gives the max height and widhth of respective x coordinate
# print(coords)
# print(rec[5]) 
columns=len(uniquex)-1
rows=len(uniquey)-1
print(columns)
print(rows)
# print(columns)

#Drawing contours wrt number of columns
# cv2.rectangle(image,(unique[0],unique[1]),(unique[0]+max_width_height[1][0],unique[1]+max_width_height[0][1]),(0,0,255),5)
# roi=base_image[y:y+max_width_height[0][1],x:x+max_width_height[1][0]]
# cv2.imwrite(os.path.join(outputs_directory,"extracted.jpg"),roi)



# cv2.imwrite(os.path.join(outputs_directory,"ContourMethod.jpg"),image)

