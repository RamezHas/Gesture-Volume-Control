import cv2
import numpy as np
import time
import HTModule as htm
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)

wcam, hcam = 640, 480
cap.set(3, wcam)
cap.set(4, hcam)

pTime = 0

detector = htm.handDetector(detectionCon=0.75)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)
minvol = volrange[0]
maxvol = volrange[1]

while True:
    success, img = cap.read()

    detector.findHands(img)
    lmList = detector.FindPosition(img)
    if len(lmList) != 0:
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        print(length)

        if length<50:
            cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)


        vol = np.interp(length,[50,300],[minvol,maxvol])
        print(vol)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)