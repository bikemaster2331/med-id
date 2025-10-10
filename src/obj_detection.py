import cv2
from ultralytics import YOLO
import sys
import os, time

# Load your trained model (replace path)
model = YOLO("ai/runs/detect/train3/weights/best.pt")

cap = cv2.VideoCapture(0)
save_dir = "output"
os.makedirs(save_dir, exist_ok=True)

def run_model(frame):
    results = model(frame, imgsz=320)

    bigbox = None
    max_area = 0

    # Draw boxes from detections
    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0]) 
            if conf > 0.5:  
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                area = (x2-x1) * (y2-y1)
                if area > max_area:
                    max_area = area
                    bigbox = (x1, y1, x2, y2, int(box.cls[0]), conf)

            
    if bigbox:
        x1, y1, x2, y2, cls, conf = bigbox
        label = f"{model.names[cls]} {conf:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # Show ret live
    cv2.imshow("YOLO Detection", frame)

    return bigbox



while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera module can't be detected")
        ans = input("Do you want to upload image instead? (Y/N): ")
        if ans.strip().lower() == "n":
            print("Exiting...")
            sys.exit()
        elif ans.strip().lower() == "y":
            image_path = input("Enter image path: ")
            frame = cv2.imread(image_path)
            if frame is None:
                print("Image not found")
                sys.exit()
            else:
                filename = f"img_capture_{int(time.time())}.jpg"
                filepath = os.path.join(save_dir, filename)
                cv2.imwrite(filepath, frame)
                run_model(frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                sys.exit()
    else:    
        bigbox = run_model(frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if bigbox:
            x1, y1, x2, y2, cls, conf = bigbox
            crop = frame[y1:y2, x1:x2]
            filename = f"video_capture_{int(time.time())}.jpg"
            filepath = os.path.join(save_dir, filename)
            cv2.imwrite(filepath, crop)
            print("Image saved")

cap.release()
cv2.destroyAllWindows()