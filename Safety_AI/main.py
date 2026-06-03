import cv2
from ultralytics import YOLO
import time
import winsound
import numpy as np # Needed for the transparency blending

model = YOLO("weights/yolo11n.pt")
cap = cv2.VideoCapture(0)

DANGER_ZONE = [0, 0, 320, 480] 
last_alert_time = 0
alert_interval = 5 

def draw_transparent_rect(img, pt1, pt2, color, alpha):
    """Creates a modern transparent overlay."""
    overlay = img.copy()
    cv2.rectangle(overlay, pt1, pt2, color, -1)
    return cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    results = model(frame, device="cuda", verbose=False)
    current_danger_detected = False

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls[0])]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            is_danger = DANGER_ZONE[0] < cx < DANGER_ZONE[2] and DANGER_ZONE[1] < cy < DANGER_ZONE[3]
            if is_danger and label == "person":
                current_danger_detected = True

            # Thin, modern bounding boxes
            color = (0, 0, 255) if is_danger else (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1) # Thin line for tech look

    # --- MODERN TRANSPARENT HUD ---
    if current_danger_detected:
        # Transparent Red Banner (Alpha 0.6)
        frame = draw_transparent_rect(frame, (0, 0), (640, 45), (0, 0, 255), 0.6)
        cv2.putText(frame, "RESTRICTED AREA BREACH", (160, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
        
        current_time = time.time()
        if current_time - last_alert_time > alert_interval:
            winsound.Beep(1200, 400)
            last_alert_time = current_time
    else:
        # Transparent Dark/Green Banner
        frame = draw_transparent_rect(frame, (0, 0), (640, 45), (0, 0, 0), 0.4)
        cv2.putText(frame, "SYSTEM STATUS: SECURE", (200, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1, cv2.LINE_AA)

    # Clean Danger Zone line
    cv2.rectangle(frame, (DANGER_ZONE[0], DANGER_ZONE[1]), (DANGER_ZONE[2], DANGER_ZONE[3]), (255, 255, 255), 1)

    cv2.imshow("Safety_AI - Modern HUD", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release()
cv2.destroyAllWindows()