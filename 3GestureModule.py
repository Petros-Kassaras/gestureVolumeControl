import cv2
import HandTrackingModule as htm
import time
import math
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL

xCam,yCam = 800, 800
cap = cv2.VideoCapture(0)
cap.set(3, xCam)
cap.set(4, yCam)
pTime =0

detector = htm.handDetector(detectionCon=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)

    if lmlist != ([],[]): # != --> not empty
        x1 ,y1 = lmlist[0][4][1], lmlist[0][4][2]
        x2, y2 = lmlist[0][8][1], lmlist[0][8][2]
        cx, cy = (x1+x2) //2, (y1+y2) //2

        cv2.circle(img, (x1,y1), 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
        cv2.line(img,(x1,y1), (x2,y2), (255, 0, 0), 3)
        cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        vol = np.interp(length,[50,300], [minVol,maxVol])
        volBar = np.interp(length,[0,30],[400,150])
        volPer = np.interp(length,[50,300],[0,100])
        volume.SetMasterVolumeLevel(vol,None)

        if length<50:
            cv2.circle(img,(cx,cy),15,(0,0,250),cv2.FILLED)

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime=cTime
            cv2.putText(img,"FPS: " + str(int(fps)),(40,50),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),3)


        cv2.imshow("Hands", img)
        if cv2.waitKey(1)==27:
            break







success, img = cap.read()
cv2.imshow("Cam", img)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()