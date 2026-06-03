import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import winsound
import threading
import time
import requests 

# 1. Setup
model = YOLO(r"C:\dev\runs\detect\Safety_AI_v1\weights\best.pt")
barrier_x = 320 

# Alarm & Email Control Variables
last_alarm_time = 0
alarm_interval = 2  # Beep every 2 seconds

last_email_time = 0
email_cooldown = 120  # Email only once every 120 seconds (2 mins)

def play_alarm():
    winsound.Beep(1000, 500)

def send_to_n8n(violation_label):
    webhook_url = "N8N_WEBHOOK_URL" 
    data = {
        "violation": violation_label,
        "status": "CRITICAL",
        "time": time.strftime("%H:%M:%S")
    }
    try:
        requests.post(webhook_url, json=data, timeout=1)
    except:
        pass

def get_modern_text(img, text, pos, color=(255, 255, 255), size=20):
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    try:
        font = ImageFont.truetype("seguisb.ttf", size) 
    except:
        font = ImageFont.load_default()
    draw.text(pos, text, font=font, fill=color)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret: break
    h, w, _ = frame.shape
    current_time = time.time()

    # UI Overlay
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 80), (20, 20, 20), -1) 
    cv2.rectangle(overlay, (0, 80), (barrier_x, h), (0, 0, 150), -1) 
    cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)

    # Barrier Line
    cv2.line(frame, (barrier_x, 80), (barrier_x, h), (0, 0, 255), 2, cv2.LINE_AA)

    results = model(frame, conf=0.4, verbose=False)[0]
    
    violations = 0
    current_label = "Unknown"
    
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = model.names[int(box.cls[0])]
        cx = (x1 + x2) // 2
        
        is_in_danger_zone = cx < barrier_x
        
        status_color = (0, 255, 100)
        if is_in_danger_zone and "NO-" in label:
            status_color = (0, 0, 255)
            violations += 1
            current_label = label # Capture label for the email
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        else:
            cv2.line(frame, (x1, y1), (x1+15, y1), status_color, 2)
            cv2.line(frame, (x1, y1), (x1, y1+15), status_color, 2)
            cv2.line(frame, (x2, y2), (x2-15, y2), status_color, 2)
            cv2.line(frame, (x2, y2), (x2, y2-15), status_color, 2)

        frame = get_modern_text(frame, label, (x1, y1-25), color=status_color, size=14)

    # Combined Logic Block
    if violations > 0:
        # 1. Beep Sound (Every 2 seconds)
        if (current_time - last_alarm_time) > alarm_interval:
            threading.Thread(target=play_alarm, daemon=True).start()
            last_alarm_time = current_time
        
        # 2. n8n Email Alert (Only once every 2 minutes)
        if (current_time - last_email_time) > email_cooldown:
            print(">>> Sending alert email via n8n...")
            threading.Thread(target=send_to_n8n, args=(current_label,), daemon=True).start()
            last_email_time = current_time

    # HUD
    frame = get_modern_text(frame, "SAFETY_AI // SECURE SYSTEM", (20, 15), size=22)
    status_msg = f"!!! VIOLATION DETECTED !!!" if violations > 0 else "ZONE CLEAR"
    msg_color = (0, 0, 255) if violations > 0 else (0, 255, 150)
    frame = get_modern_text(frame, status_msg, (20, 45), color=msg_color, size=16)

    cv2.imshow("Safety_AI: Audio Alert System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
