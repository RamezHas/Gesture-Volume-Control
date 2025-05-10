import cv2
import numpy as np
import time
import HTModule as htm
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize camera
cap = cv2.VideoCapture(0)

wcam, hcam = 640, 480
cap.set(3, wcam)
cap.set(4, hcam)

pTime = 0

# Initialize hand detector
detector = htm.handDetector(detectionCon=0.75)

# Initialize volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volrange = volume.GetVolumeRange()

minvol = volrange[0]
maxvol = volrange[1]

try:
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read from camera. Exiting loop.")
            break

        detector.findHands(img)
        lmList = detector.FindPosition(img)
        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)
            print(length)

            if length < 50:
                cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

            vol = np.interp(length, [50, 300], [minvol, maxvol])
            print(int(length), vol)
            volume.SetMasterVolumeLevel(vol, None)

        cTime = time.time()
        fps = 1 / (cTime - pTime) if cTime != pTime else 0
        pTime = cTime

        cv2.putText(
            img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3
        )
        cv2.imshow("Image", img)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting on user request ('q' pressed).")
            break

except KeyboardInterrupt:
    print("\nInterrupted by user (Ctrl+C). Exiting gracefully.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Camera released and all windows closed.")