# ✋🔊 Hand Gesture Volume Control

Welcome to **Hand Gesture Volume Control** – a seamless, touch-free way to control your computer’s audio volume using nothing but your hand gestures and your webcam! 🎥🖐️

---

## 🚀 Features

- **Real-time Hand Tracking** 🖐️
- **Smooth Volume Adjustment** 🔊
- **Visual Feedback** 🎯 (see your gestures and volume changes on-screen)
- **Graceful Exit & Error Handling** ✅

---

## 🛠️ Requirements

- Python 3.7+
- Webcam (internal or external)
- The following Python libraries:
  - `opencv-python`
  - `numpy`
  - `mediapipe`
  - `pycaw`
  - `comtypes`

> ℹ️ To install dependencies, run:
```shell script
pip install opencv-python numpy mediapipe pycaw comtypes
```


---

## 📦 How It Works

1. **Start the App:**  
   Launch the script – your webcam activates automatically.
2. **Show Your Hand:**  
   Place your hand in front of the camera. The script will outline your hand and fingertips.
3. **Use Gesture to Change Volume:**  
   - Pinch your thumb and index finger together to decrease the volume.
   - Spread your thumb and index finger apart to increase the volume.
   - Visual cues help you gauge the current volume level.
4. **Exit:**  
   - Press `q` in the video window to safely close the app.

---

## 🖥️ Usage

```shell script
python gvc.py
```


### ✋ Controls

- **Pinch:** Decrease volume
- **Spread:** Increase volume
- **Press `q`:** Quit application

---

## 🌟 Demo


---

## ⚠️ Disclaimer

- Works best with good lighting and a clear background.
- Windows-only due to `pycaw` library.
- Your webcam must be accessible by OpenCV.

---

## 🧑‍💻 Credits

- [MediaPipe](https://google.github.io/mediapipe/)
- [Pycaw](https://github.com/AndreMiras/pycaw)
- [OpenCV](https://opencv.org/)

---

## 💡 Inspiration

A fun, practical demo combining media processing and computer vision for creative remote control interfaces!

---

🙌 **Enjoy touch-free audio control and happy coding!**
