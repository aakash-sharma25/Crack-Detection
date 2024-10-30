import cv2
import numpy as np

def detect_cracks(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Edge detection (using Canny as a basic example for crack edges)
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours from edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    crack_detected = False
    for contour in contours:
        # Filter out small contours to ignore noise
        if cv2.contourArea(contour) > 100:
            crack_detected = True
            
            # Draw a blue bounding box around the crack
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue box
            
            # Draw a red contour outline around the crack
            cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)  # Red contour

    return frame, crack_detected

# Access the camera (0 is usually the default camera)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detect cracks in the current frame
    processed_frame, crack_detected = detect_cracks(frame)
    
    # Display a message if a crack is detected
    if crack_detected:
        cv2.putText(processed_frame, "Crack Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Show the processed frame
    cv2.imshow("Crack Detection", processed_frame)

    # Exit loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
