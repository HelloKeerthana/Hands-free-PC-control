# gesture-based mouse control

## overview
this project implements a gesture-based mouse control system using opencv, mediapipe, and pyautogui. 
it allows users to control the mouse cursor and perform various actions such as left click, right click, double click, and taking screenshots using hand gestures.

## features
- hand tracking using mediapipe
- cursor movement based on index finger position
- left and right click detection
- double click functionality
- gesture-based screenshot capture

## feature control
- move mouse : just the index finger & no thumb
- left click : thumb & middle fingers up + index finger down
- right click : thumb & index fingers up + middle finger down
- double click : thumb up, middle & index finger down
- screenshot : all 3 fingers closed (as a rock)

## requirements
- python < 3.10.0
- opencv
- mediapipe
- pyautogui
- pynput
- numpy

## installation
```sh
pip install opencv-python==4.5.3.56 mediapipe==0.8.6.2 pyautogui==0.9.53 pynput==1.7.3 numpy==1.21.0
```

## usage
```sh
python gesture_control.py
```
## exit
press `q` to exit the application.
