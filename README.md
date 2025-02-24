# Gesture-Based Mouse Control

## Overview
This project implements a gesture-based mouse control system using OpenCV, MediaPipe, and PyAutoGUI. 
It allows users to control the mouse cursor and perform various actions such as left click, right click, double click, and taking screenshots using hand gestures.

## Features
- Hand tracking using MediaPipe
- Cursor movement based on index finger position
- Left and right click detection
- Double click functionality
- Gesture-based screenshot capture

## feature Control
- move mouse : just the index finger & no thumb
- left click : thumb & middle fingers up + index finger down
- right click : thumb & index fingers up + middle finger down
- double click : thumb up, middle & index finger down
- screenshot : all 3 fingers closed (as a rock)

## Requirements
- Python < 3.10.0
- OpenCV
- MediaPipe
- PyAutoGUI
- Pynput
- Numpy

## Installation
```sh
pip install opencv-python==4.5.3.56 mediapipe==0.8.6.2 pyautogui==0.9.53 pynput==1.7.3 numpy==1.21.0
```

## Usage
```sh
python gesture_control.py
```
## Exit
Press `q` to exit the application.
