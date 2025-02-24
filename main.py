import cv2
import mediapipe as mp 
import pyautogui 
import random 
import numpy as np
from pynput.mouse import Button, Controller

cursor = Controller()

screen_w, screen_h = pyautogui.size()

def compute_angle(p1, p2, p3):
    rad = np.arctan2(p3[1] - p2[1], p3[0] - p2[0]) - np.arctan2(p1[1] - p2[1], p1[0] - p2[0])
    return np.abs(np.degrees(rad))

def compute_distance(points):
    if len(points) < 2:
        return 0
    (x1, y1), (x2, y2) = points[0], points[1]  
    dist = np.hypot(x2 - x1, y2 - y1)  
    return np.interp(dist, [0, 1], [0, 1000])  

mpHands = mp.solutions.hands
hand_tracker = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

def extract_index_tip(hand_data):
    if hand_data.multi_hand_landmarks:
        return hand_data.multi_hand_landmarks[0].landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None  

def move_cursor(index_tip):
    if index_tip:
        x = min(max(int(index_tip.x * screen_w), 0), screen_w)
        y = min(max(int(index_tip.y / 2 * screen_h), 0), screen_h)
        pyautogui.moveTo(x, y)

def detect_left_click(points, thumb_index_sep):
    return (
        compute_angle(points[5], points[6], points[8]) < 50 and
        compute_angle(points[9], points[10], points[12]) > 90 and
        thumb_index_sep > 50
    )

def detect_right_click(points, thumb_index_sep):
    return (
        compute_angle(points[9], points[10], points[12]) < 50 and
        compute_angle(points[5], points[6], points[8]) > 90 and
        thumb_index_sep > 50
    )

def detect_double_click(points, thumb_index_sep):
    return (
        compute_angle(points[5], points[6], points[8]) < 50 and
        compute_angle(points[9], points[10], points[12]) < 50 and
        thumb_index_sep > 50
    )

def detect_screenshot(points, thumb_index_sep):
    return (
        compute_angle(points[5], points[6], points[8]) < 50 and
        compute_angle(points[9], points[10], points[12]) < 50 and
        thumb_index_sep < 50
    )

def analyze_gesture(frame, points, hand_data):
    if len(points) >= 21:
        index_tip = extract_index_tip(hand_data)
        thumb_index_sep = compute_distance([points[4], points[5]]) or 0

        if compute_distance([points[4], points[5]]) < 50 and compute_angle(points[5], points[6], points[8]) > 90:
            move_cursor(index_tip)
        elif detect_left_click(points, thumb_index_sep):
            cursor.press(Button.left)
            cursor.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif detect_right_click(points, thumb_index_sep):
            cursor.press(Button.right)
            cursor.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif detect_double_click(points, thumb_index_sep):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif detect_screenshot(points, thumb_index_sep):
            snap = pyautogui.screenshot()
            label = random.randint(1, 1000)
            snap.save(f'screenshot_{label}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

def run():
    drawer = mp.solutions.drawing_utils
    cam = cv2.VideoCapture(0)
    
    try:
        while cam.isOpened():
            ret, frame = cam.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hand_data = hand_tracker.process(rgb_frame)

            points = []
            if hand_data.multi_hand_landmarks:
                landmarks = hand_data.multi_hand_landmarks[0]
                drawer.draw_landmarks(frame, landmarks, mpHands.HAND_CONNECTIONS)
                for lm in landmarks.landmark:
                    points.append((lm.x, lm.y))

            analyze_gesture(frame, points, hand_data)

            cv2.imshow('Hand Tracker', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
