import os
import cv2
import pytesseract as pi
import LineDetector

#Assigning Directories
outputs_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Outputs")
images_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Testing Images")
os.chdir(images_directory)


#Getting Output Image and the list of points of the line segments
image=cv2.imread("6.jpg")
result=pi.image_to_string(image)
print(result)
output_image,lines=LineDetector.linedetector(image)
cv2.imshow("Output",output_image)
cv2.waitKey(0)


#Printing Output Lines
line=[]
for i in lines:
    line.append(list(i[0]))
# print(line)


#Applying OCR
result=pi.image_to_string(output_image)
file=open(os.path.join(outputs_directory,"Results.txt"),'w')
file.write(result)
file.close()


# Converting the stored File in list
file=open(os.path.join(outputs_directory,"Results.txt"),'r')
list=(file.readlines())
column_Names=[]

for column in list[0].split(" "):
    column_Names.append(column)
print(column_Names)
