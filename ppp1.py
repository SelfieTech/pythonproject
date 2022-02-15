import cv2
import numpy as np
import ppp3 as htm
import time
import autopy

##########################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 7
#########################

plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(maxHands=1)
wScr , hScr = autopy.screen.size()
print(wScr,hScr)
while True:
    # 1. find hand landmark
    success, img = cap.read()
    img = detector.findHands(img)
    lmList,bbox = detector.findPosition(img)
    # 2. get the tip of the index and middle fingers
    if len(lmList)!=0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        #print(x1,y1,x2,y2)



        # 3. check which fingers are up
        fingers= detector.fingersUp()
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,0),2)



        # 4. only index finger : moving mode
        if fingers[1]==1 and fingers[2]==0:
            # 5. convert coordinates
            x3 = np.interp(x1, (frameR,wCam-frameR),(0,wScr))
            y3 = np.interp(y1, (frameR,hCam-frameR),(0,hScr))
            # 6. smoothen the values
            clocX=plocX + (x3-plocX) / smoothening
            clocY=plocY + (y3-plocY) / smoothening
            # 7. move mouse
            autopy.mouse.move(wScr-clocX, clocY)
            cv2.circle(img,(x1,y1),15,(255,0,0),cv2.FILLED)
            plocX, plocY = clocX, clocY
        # 8. both index and middle fingers are up then it is in clicking mode
        if fingers[1]==1 and fingers[2]==1:
            # 9. find distance between fingers
            length, img, infoLine = detector.findDistance(8,12,img)
            print(length)
            # 10. click mouse if distance is short
            if length < 40 :
                cv2.circle(img,(infoLine[4],infoLine[5]),15,(0,255,0),cv2.FILLED)
                autopy.mouse.click()
        
        
        # 11. frame rate
    cTime =time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    # 12. display
    cv2.imshow("Image", img)
    cv2.waitKey(1)