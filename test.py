import cv2
import numpy as np
import time
import HTModule as htm

cap = cv2.VideoCapture(0)

wcam, hcam = 640, 480
cap.set(3, wcam)
cap.set(4, hcam)

pTime = 0

detector = htm.handDetector(detectionCon=0.75)

while True:
    success, img = cap.read()

    detector.findHands(img)
    lmList = detector.FindPosition(img)
    if len(lmList) != 0:
        print(lmList[4])

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
