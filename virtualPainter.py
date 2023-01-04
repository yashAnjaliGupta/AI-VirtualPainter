import cv2
import time 
import handTrackingModule as htm 
import os 
import numpy as np 

folderPath="Headers"
myList=os.listdir(folderPath)
# print(myList)

overlayList=[]

for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
    
# print(len(overlayList))
header=overlayList[0]
drawColor=(0,0,255)
xp,yp=0,0
imgCanvas=np.zeros((720,1280,3),np.uint8)

################################################
wCam,hCam=1280,720
brushThickness=15
eraserThicknes=50
################################################
cap=cv2.VideoCapture(1)
cap.set(3,wCam)
cap.set(4,hCam)

detector=htm.handDetector(detectionCon=0.8)

while True:
    #import image
    success,img=cap.read()
    img[0:100,0:1280]=header
    # img=cv2.flip(img,1)
    # find Hand landmarks
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if(len(lmList)!=0):
        # tip of index and middle finger
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
    # check fingers up
        fingers=detector.fingersUp()
        # print(fingers) 
    # selection mode 
        if fingers[1] and fingers[2]:
            cv2.rectangle(img,(x1,y1-20),(x2,y2+20),drawColor,cv2.FILLED)
            # print("selection mode")
            xp,yp=0,0
            if(y1<100):
                # print(x1)
                if 20<=x1<=120:
                    header=overlayList[0]
                    drawColor=(0,0,255)
                elif 280<=x1<=380:
                    header=overlayList[1]
                    drawColor=(0,255,0)
                elif 530<=x1<=630:
                    header=overlayList[2]
                    drawColor=(255,0,0)
                elif 1140<=x1<=1260:
                    header=overlayList[3]
                    drawColor=(0,0,0)
    # drawing mode
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            # print("drawing mode")
            if xp==0 and yp==0:
                xp,yp=x1,y1
            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThicknes)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThicknes)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)
            xp,yp=x1,y1
    # img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv =cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)
    
    
    cv2.imshow("IMAGE",img)
    cv2.imshow("CANVAS",imgCanvas)
    cv2.waitKey(1)


    