import cv2
from pytesseract import *
import os
import modules.roi as ROI
import pandas as pd
import argparse
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from tabulate import tabulate

#Assigning Directories
outputs_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Outputs")
images_directory=os.path.join(os.path.join(os.getcwd(),"OCR"),"Testing Images")
os.chdir(images_directory)


#Getting Output Image and the list of points of the line segments
image=cv2.imread("2.jpg")
image=ROI.roi(image)
result = image_to_data(cv2.cvtColor(image,cv2.COLOR_BGR2RGB),config="--psm 3", output_type=Output.DICT)
coords=[]
text=[]
for i in range(0,len(result['text'])):

    x=result['left'][i]
    y=result["top"][i]
    w=result["width"][i]
    h=result["height"][i]

    confidence=result['conf'][i]
    if(confidence>0):

        coords.append((x,y,w,h))
        text.append(result['text'][i])

xCoords=[(c[0],0) for c in coords]

# Applying Clustering

# clustering = AgglomerativeClustering(
# 	n_clusters=None,
# 	affinity="manhattan",
# 	linkage="complete",
# 	distance_threshold=25.0)
# clustering.fit(xCoords)
# sortedClusters=[]

# for l in np.unique(clustering.labels_):
        
# 	idxs = np.where(clustering.labels_ == l)[0]
# 	if len(idxs) > 2:
# 		avg = np.average([coords[i][0] for i in idxs])
# 		sortedClusters.append((l, avg))
# sortedClusters.sort(key=lambda x: x[1])
# df = pd.DataFrame()

# # loop over the clusters again, this time in sorted order
# for (l, _) in sortedClusters:
# 	idxs = np.where(clustering.labels_ == l)[0]
# 	yCoords = [coords[i][1] for i in idxs]
# 	sortedIdxs = idxs[np.argsort(yCoords)]

# 	color = np.random.randint(0, 255, size=(3,), dtype="int")
# 	color = [int(c) for c in color]
# 	for i in sortedIdxs:
# 		(x, y, w, h) = coords[i]
# 		cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
# 	cols = [text[i].strip() for i in sortedIdxs]
# 	currentDF = pd.DataFrame({cols[0]: cols[1:]})
# 	df = pd.concat([df, currentDF], axis=1)
	
# df.fillna("", inplace=True)
# print(tabulate(df, headers="keys", tablefmt="psql"))
# # write our table to disk as a CSV file
# print("[INFO] saving CSV file to disk...")
# df.to_csv("result.csv", index=False)


for i in range(0,len(coords)):
    (x,y,w,h)=coords[i]
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)


cv2.imwrite("OCR_RESULT.jpg",image)


#Saving Results
# file=open(os.path.join(outputs_directory,"Results.txt"),'w')
# file.write(result)
# file.close()



