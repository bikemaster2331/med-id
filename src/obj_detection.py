import cv2
from ultralytics import YOLO
import sys

# Load your trained model (replace with your path)
model = YOLO("ai/runs/detect/train5/weights/best.pt")

cap = cv2.VideoCapture(0)


def run_model(frame):
    results = model(frame, imgsz=320)

    # Draw boxes from detections
    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0])   # confidence
            if conf > 0.1:  # only keep detections with >80% confidence
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cls = int(box.cls[0])   # class id
                label = f"{model.names[cls]} {conf:.2f}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # Show result live
    cv2.imshow("YOLO Detection", frame)



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
                run_model(frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                sys.exit()
    else:
        run_model(frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()