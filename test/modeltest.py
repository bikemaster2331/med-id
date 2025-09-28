import cv2
from ultralytics import YOLO
import sys

# Load your trained model
model = YOLO("ai/runs/detect/train5/weights/best.pt")

# Ask for an image path
if len(sys.argv) > 1:
    image_path = sys.argv[1]
else:
    image_path = input("Enter image path: ")

# Load image
image = cv2.imread(image_path)
if image is None:
    print("Image not found.")
    sys.exit()

# Run YOLO inference
results = model(image, imgsz=320)

# Draw results on image
for r in results:
    for box in r.boxes:
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls = int(box.cls[0])
        label = f"{model.names[cls]} {conf:.2f}"

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Show result
cv2.imshow("YOLO Test", image)
print("Press any key to close window...")
cv2.waitKey(0)
cv2.destroyAllWindows()
