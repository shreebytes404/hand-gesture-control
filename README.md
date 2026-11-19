# Hand Gesture Control

Control your computer with hand gestures using a webcam. Built with Python, OpenCV and MediaPipe.

## Projects
- **AI Virtual Mouse** (`virtual_mouse.py`): move the cursor, click and scroll with your hand.
- **Volume Control** (`volumecontrol.py`): change the system volume with hand gestures.

## Virtual mouse gestures
| Gesture | Action |
|---|---|
| Index finger up | Move cursor |
| Index + middle finger pinched together | Click |
| Index + middle + ring finger up | Scroll up |
| Index + middle + ring + pinky up | Scroll down |

Press ESC on the camera window to quit.

## Setup
    pip install -r requirements.txt

## Run
    python virtual_mouse.py
    python volumecontrol.py

## Notes
- `new_detect.py` is the hand-tracking module both scripts use.
- If the wrong camera opens, change `cv2.VideoCapture(1)` to `cv2.VideoCapture(0)`.

## Tech
Python, OpenCV, MediaPipe, NumPy, autopy, pyautogui