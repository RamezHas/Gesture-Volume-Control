import cv2
import numpy as np
import time

import HTModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import threading
import speech_recognition as sr

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


volume_control_enable=False
cmd_lock=threading.Lock()
def listen_cmds():
    global volume_control_enable
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("started. say 'enable' or 'disable' to control volume control")
    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)
        try:
            cmd = recognizer.recognize_google(audio).lower()
            print(f"Recognized command: {cmd}")
            if "enable" in cmd:
                volume_control_enable = True
                print("Volume control enabled")
            elif "disable" in cmd:
                with cmd_lock:
                    volume_control_enable = False
                    print("Volume control disabled")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
voint_control_thread = threading.Thread(target=listen_cmds)
voint_control_thread.start()

try:
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read from camera. Exiting loop.")
            break

        detector.findHands(img)
        lmList = detector.FindPosition(img)

        with cmd_lock:
            enable_vc = volume_control_enable
        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)
            if enable_vc:
                if length < 50:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

                vol = np.interp(length, [50, 300], [minvol, maxvol])
                print(int(length), vol)
                volume.SetMasterVolumeLevel(vol, None)
            else:
                cv2.putText(img, "Volume control disabled", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

        cTime = time.time()
        fps = 1 / (cTime - pTime) if cTime != pTime else 0
        pTime = cTime

        cv2.putText(
            img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3
        )
        status = "ON" if enable_vc else "OFF"
        cv2.putText(img,f'volume control: {status}',(20,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
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