import cv2
import mediapipe as mp
import HandDetector
import math
import numpy as np
from ctypes import cast,POINTER
import ctypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume = cast(interface,POINTER(IAudioEndpointVolume))
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

WebCamWidth = 1280
WebCamHeight = 720
cap = cv2.VideoCapture(0)
cap.set(3,WebCamWidth)
cap.set(4,WebCamHeight)
detecotr = HandDetector.HandDetector()
while True:
    success,img = cap.read()
    img = detecotr.findHands(img)
    lmList = detecotr.findPosition(img,draw = False)

    if len(lmList) != 0:
        fingers = detecotr.fingersUp(lmList)
        print(fingers)
        if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            ctypes.windll.user32.LockWorkStation()
        x1,y1 = lmList[4][1], lmList[4][2] # coordinates of finger 1
        x2,y2 = lmList[8][1], lmList[8][2] # coordinates of finger 2
        cx,cy = (x1+x2)//2,(y1+y2)//2 # center of the line3
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        lengthOFLine = math.hypot(x2-x1,y2-y1)

        # Hand range 50 to 300
        # Volume range -65 to 0

        vol = np.interp(lengthOFLine,[50,300],[minVol,maxVol])
        volBar = np.interp(lengthOFLine, [50, 300], [400, 150])
        volPercentage = np.interp(lengthOFLine,[50,300],[0,100])
        volume.SetMasterVolumeLevel(vol, None)

        cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img,f'{int(volPercentage)}%',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.imshow("Img",img)
    cv2.waitKey(1)