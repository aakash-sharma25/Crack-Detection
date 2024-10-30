import cv2
import numpy as np
import os
from ultralytics import YOLO

# Load the YOLO model (ensure you provide the correct path to your .pt file)
model = YOLO("yolov8n.pt")  # Update with the correct path

def detect_crack(image_path):
    """Detects cracks in the image using Canny edge detection."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image at path {image_path} could not be loaded.")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    crack_length = np.sum(edges == 255)
    
    # Highlight cracks in the image
    img[edges == 255] = [0, 0, 255]  # Marking cracks in red
    result_image_path = os.path.join("processed", os.path.basename(image_path).replace('.', '_crack.'))
    cv2.imwrite(result_image_path, img)
    
    return crack_length, result_image_path

def detect_objects(image_path):
    """Detects objects in the image using YOLO model."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image at path {image_path} could not be loaded.")
    
    results = model(img)
    detected_objects = []
    
    boxes = results[0].boxes  
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = box.conf[0].item()
        class_id = int(box.cls[0].item())
        label = model.names[class_id]
        detected_objects.append({
            'label': label,
            'confidence': confidence,
            'box': [x1, y1, x2, y2]
        })
        
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(img, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    result_image_path = os.path.join("processed", os.path.basename(image_path).replace('.', '_detected.'))
    cv2.imwrite(result_image_path, img)

    return detected_objects, result_image_path

def detect_cracks(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    crack_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > 100:
            crack_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)
    return frame, crack_detected

def gen_frames():
    cap = cv2.VideoCapture(0)  
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame, crack_detected = detect_cracks(frame)
        if crack_detected:
            cv2.putText(processed_frame, "Crack Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()
