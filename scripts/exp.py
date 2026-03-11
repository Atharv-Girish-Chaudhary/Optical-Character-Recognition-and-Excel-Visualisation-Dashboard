
    # xcoords=sorted(xcoords)
    # ycoords=sorted(ycoords)

    # #Adding elements to the dictionary of 'x' 
    # '''Explaination of rec: Stores all the related width and heights of bounding boxes 
    #    originating from that 'x' coordinate.'''

    # for c in coords:                                    #'c' in this context, are the coordinates of the bounding box.
    #     x = c[0]                                        #This chooses the x coordinate from that bouding box 'c'.
    #     if x not in rec:
    #         rec[x]=[[c[2],c[3]]]                        #Chooses the width and height from that bouding box 'c'.
    #     else:
    #         rec[x].append([c[2],c[3]])
    
    # # Finding the unique x coordinate 
    # for i in xcoords:
    #     if(i in unique_x):
    #         pass
    #     elif(xcoords.count(i)>=1):
    #         unique_x.append(i)

    # #Finding the unique y coordinate 
    # for i in ycoords:
    #     if(i in unique_y):
    #         pass
    #     elif(ycoords.count(i)>=1):
    #         unique_y.append(i)

    # #Finding max width for the x_coordinate
    # for x in unique_x:
    #     mw,mh=[],[]
    #     for r in rec[x]:    
    #         mw.append(r[0])  
    #     max_width.append(max(mw))

    # #Calculating the values of no of columns and rows and max_height
    # columns=len(unique_x)-1
    # rows=len(unique_y)-1
    # max_height=max(heights)