import cv2
import numpy as np
import math

path= "1.jpg"
img= cv2.imread(path)
pointsList =[]
def mousePoint(event,x,y,flag,params):
    if event == cv2.EVENT_LBUTTONDOWN:
        size = len(pointsList)
        if size !=0 and size%3 !=0:
            cv2.line(img,tuple(pointsList[round((size-1)/3)*3]),(x,y),(0,0,255),1)
        cv2.circle(img,(x,y), 3,(0,0,255),cv2.FILLED)
        pointsList.append([x,y])
        print(pointsList)
        #print(x,y)

def gradient(pt1,pt2):
    if(pt2[0]-pt1[0]!=0):
        return (pt2[1]-pt1[1])/(pt2[0]-pt1[0])
    if(pt2[0]-pt1[0]==0):
        return 0

def getAngle(pointsList):
    pt1,pt2, pt3= pointsList[-3:]
    if(pt2[0]-pt1[0]==0) and (pt2[1]-pt1[1]==0):
        cv2.putText(img, '90' ,(pt1[0]-40,pt1[1]-20),cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),2)
    if(pt2[0]-pt1[0]!=0) and (pt2[1]-pt1[1]!=0):
        # print(pt1,pt2,pt3)
        m1=gradient(pt1,pt2)
        m2=gradient(pt1,pt3)
        # angR = abs(math.atan((m2-m1) / (1+(m1*m2))))
        angR = abs(math.atan((m2-m1) / (1+(m1*m2))))
        angD = round(math.degrees(angR))
        #print(angD)
        cv2.putText(img, str(angD),(pt1[0]-40,pt1[1]-20),cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),2)

while True:

    if(len(pointsList) % 3==0) and len(pointsList) != 0:
        getAngle(pointsList)
    cv2.imshow("Image",img)
    cv2.setMouseCallback("Image", mousePoint)
    if cv2.waitKey(1)& 0xFF == ord('q'):
        pointsList=[]
        img= cv2.imread(path)
        break