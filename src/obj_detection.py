import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)


img_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, stream=True, imgsz=160)

    for r in results:
        if len(r.boxes) == 0:
            continue  # no detections

        # Track the largest box
        largest_box = None
        max_area = 0

        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # coords
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            area = (x2 - x1) * (y2 - y1)  # box area

            if area > max_area:
                max_area = area
                largest_box = (x1, y1, x2, y2, float(box.conf[0]), int(box.cls[0]))

        # Draw only the largest box
        if largest_box:
            x1, y1, x2, y2, conf, cls = largest_box
            label = f"{model.names[cls]} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)


    cv2.imshow("Largest Object Only", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
