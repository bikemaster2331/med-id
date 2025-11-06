import cv2
from ultralytics import YOLO
import sys
import os
import time
from collections import deque
import numpy as np
import json
from paddleocr import PaddleOCR

# --- Configuration Constants (Now defined globally, referenced in class) ---
# These remain outside the class as project-wide settings that can be accessed globally
CONF_THRESHOLD = 0.75 
CONF_THRESHOLD_IMAGE = 0.60  
MIN_DETECTION_AREA = 5000  
MIN_DETECTION_AREA_IMAGE = 2000  
STABILITY_FRAMES = 5 
COOLDOWN_SECONDS = 3  
MODEL_PATH = "ai/runs/detect/train5/weights/best.pt"
SAVE_DIR = "output"

# --- Global Components ---
# These are loaded once and globally available since they represent physical hardware/model
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"ERROR: Could not load YOLO model at {MODEL_PATH}. {e}")
    sys.exit()

cap = cv2.VideoCapture(0)
os.makedirs(SAVE_DIR, exist_ok=True)


# --- Precaution Function (Remains outside the class for startup) ---
def precaution():
    print("This app provides general information about medicines. \nWe are not medical professionals, and this does not replace professional advice. \nAlways consult a healthcare provider before taking any medicine.\nBy using this app, you agree to use it at your own risk.")

    while True:
        choice = input("Do you want to continue? (Y/N): ").lower()
        if choice == "y":
            print("Welcome to Med-ID, please continue to the next process.")
            return True
        elif choice == "n":
            print("Exiting..")
            return False
        else:
            print("Not defined")

# --- Main Application Class ---
class MedicineApp:

    def __init__(self, model_instance, capture_instance):
        # Tracking variables moved to instance attributes (self.)
        self.model = model_instance
        self.cap = capture_instance
        self.save_dir = SAVE_DIR
        self.history = deque(maxlen=STABILITY_FRAMES)
        
        # Tracking variables
        self.last_save_time = 0
        self.last_class_detected = None
        
        # Configuration variables (can be adjusted via input)
        self.conf_thresh = CONF_THRESHOLD
        self.min_area = MIN_DETECTION_AREA
        self.cooldown = COOLDOWN_SECONDS

    # --- Utility Methods ---

    def calculate_iou(self, box1, box2):
        """Calculate Intersection over Union between two boxes"""
        x1_1, y1_1, x2_1, y2_1 = box1
        x1_2, y1_2, x2_2, y2_2 = box2

        # Calculate intersection area
        x_left = max(x1_1, x1_2)
        y_top = max(y1_1, y1_2)
        x_right = min(x2_1, x2_2)
        y_bottom = min(y2_1, y2_2)

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        # Calculate union area
        box1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
        box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
        union_area = box1_area + box2_area - intersection_area

        return intersection_area / union_area if union_area > 0 else 0

    def is_stable_detection(self, current_box, history, iou_threshold=0.6):
        """Check if detection is stable across frames"""
        if len(history) < STABILITY_FRAMES:
            return False

        # Check if all recent detections are of the same class
        classes = [h[4] for h in history]
        if len(set(classes)) > 1:
            return False

        # Check if boxes are stable (high IoU with each other)
        for prev_box in history:
            if self.calculate_iou(current_box[:4], prev_box[:4]) < iou_threshold:
                return False

        return True

    def apply_nms_custom(self, boxes, iou_threshold=0.5):
        """Apply Non-Maximum Suppression to remove overlapping boxes"""
        if len(boxes) == 0:
            return []

        # Sort by confidence
        boxes = sorted(boxes, key=lambda x: x[5], reverse=True)

        keep = []
        while len(boxes) > 0:
            keep.append(boxes[0])
            boxes = [box for box in boxes[1:]
                    if self.calculate_iou(keep[-1][:4], box[:4]) < iou_threshold]

        return keep

    # --- Core Processing Methods ---

    def run_model(self, frame, debug_mode=False, use_image_thresholds=False):
        
        # Use instance attributes for thresholds
        conf_thresh = CONF_THRESHOLD_IMAGE if use_image_thresholds else self.conf_thresh
        area_thresh = MIN_DETECTION_AREA_IMAGE if use_image_thresholds else self.min_area

        # Run inference
        results = self.model(frame, imgsz=320, conf=0.5, iou=0.4)

        all_detections = []
        rejected_detections = []

        # Collect all valid detections
        for r in results:
            for box in r.boxes:
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                area = (x2 - x1) * (y2 - y1)
                cls = int(box.cls[0])

                rejection_reason = None

                # Apply stricter confidence threshold
                if conf <= conf_thresh:
                    rejection_reason = f"Low confidence: {conf:.3f} <= {conf_thresh}"
                # Filter by minimum area
                elif area <= area_thresh:
                    rejection_reason = f"Small area: {area}px <= {area_thresh}px"
                else:
                    all_detections.append((x1, y1, x2, y2, cls, conf))

                if rejection_reason and debug_mode:
                    rejected_detections.append((self.model.names[cls], conf, area, rejection_reason))

        if debug_mode and rejected_detections:
            print("\n[DEBUG] Rejected detections:")
            for name, conf, area, reason in rejected_detections:
                print(f"  ❌ {name}: {reason}")
        
        if debug_mode:
            print(f"[DEBUG] Passed filters: {len(all_detections)} detections")

        # Apply custom NMS
        filtered_detections = self.apply_nms_custom(all_detections)

        # Find the largest detection
        bigbox = None
        max_area = 0
        
        for detection in filtered_detections:
            x1, y1, x2, y2, cls, conf = detection
            area = (x2 - x1) * (y2 - y1)
            if area > max_area:
                max_area = area
                bigbox = detection

        # Draw detections and stability info
        for detection in filtered_detections:
            x1, y1, x2, y2, cls, conf = detection
            color = (0, 255, 0) if detection == bigbox else (255, 0, 0)
            thickness = 2 if detection == bigbox else 1
            
            label = f"{self.model.names[cls]} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
            cv2.putText(frame, label, (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Check for stable detection
        is_stable = False
        if bigbox:
            self.history.append(bigbox)
            is_stable = self.is_stable_detection(bigbox, self.history)

            # Add stability indicator
            if is_stable:
                cv2.putText(frame, "STABLE", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                remaining = STABILITY_FRAMES - len(self.history)
                cv2.putText(frame, f"Stabilizing... {remaining}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
        else:
            self.history.clear()

        # Show confidence threshold info
        cv2.putText(frame, f"Conf: {self.conf_thresh:.2f} | Area: {self.min_area}", 
                (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow("YOLO Detection", frame)

        return bigbox, is_stable

    def save_detection(self, frame, bigbox, bypass_cooldown=False):
        """Save detection with cooldown to prevent spam"""
        
        current_time = time.time()
        x1, y1, x2, y2, cls, conf = bigbox

        # Check cooldown (uses self.last_save_time)
        if not bypass_cooldown and current_time - self.last_save_time < self.cooldown:
            print(f"Cooldown active. Wait {self.cooldown - (current_time - self.last_save_time):.1f}s")
            return False

        # Save cropped image (logic simplified slightly for context)
        padding = 20
        h, w = frame.shape[:2]
        y1_pad = max(0, y1 - padding)
        y2_pad = min(h, y2 + padding)
        x1_pad = max(0, x1 - padding)
        x2_pad = min(w, w, x2 + padding) # Fixed issue with x2_pad logic
        crop_padded = frame[y1_pad:y2_pad, x1_pad:x2_pad]

        # Save with class name in filename
        class_name = self.model.names[cls]
        filename = f"{class_name}_{int(current_time)}_conf{conf:.2f}.jpg"
        filepath = os.path.join(self.save_dir, filename)
        cv2.imwrite(filepath, crop_padded)

        self.last_save_time = current_time
        self.last_class_detected = cls
        print(f"✅ Saved: {filename}")
        return True
    
    def text_extract(self, frame):
        ocr = PaddleOCR(use_angle_cls = True, lang='en')
        result = ocr.predict(self.frame)
        extracted_text = []
        if result and len(result) > 0:
            result_dict = result[0]
            if 'rec_texts' in result_dict and 'rec_scores' in result_dict:
                texts = result_dict['rec_texts']
                score = result_dict['rec_scores']
                for i, (text, confidence) in enumerate(zip(texts, score)):
                    if confidence > 0.8:
                        extracted_text.append({
                            "text": text,
                            "confidence": confidence
                        })
            else:
                print("No text found")
        else:
            print("OCR failed, try again")
        self.save_to_json(extracted_text)
        return extracted_text

    def start_detection(self):
        """The main execution loop for the video stream."""
        print("Starting detection...")
        print(f"Settings: Confidence={self.conf_thresh}, MinArea={self.min_area}, Stability={STABILITY_FRAMES} frames")
        print("Press 'q' to quit, 's' to force save, 'c' to adjust confidence")

        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("❌ Camera not detected")
                ans = input("Upload image instead? (Y/N): ").strip().lower()

                if ans == "n":
                    print("Exiting...")
                    sys.exit()
                elif ans == "y":
                    image_path = input("Enter image path: ").strip()
                    self.frame = cv2.imread(image_path)

                    if self.frame is None:
                        print("❌ Image not found")
                        return False
                    else:
                        bigbox, is_stable = self.run_model(self.frame, debug_mode=True, use_image_thresholds=True)
                        if bigbox:
                            print(f"📸 Static image mode - saving without stability check")
                            self.save_detection(self.frame, bigbox, bypass_cooldown=True)
                            self.text_extract(self.frame)
                        else:
                            print("❌ No valid detections found")
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        sys.exit()
            else:
                bigbox, is_stable = self.run_model(frame)

                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break
                elif key == ord("s") and bigbox:
                    # Force save
                    self.save_detection(frame, bigbox, bypass_cooldown=True) # Bypass cooldown for force save
                elif key == ord("c"):
                    # Adjust confidence threshold (needs access to self.conf_thresh)
                    new_conf = input("Enter new confidence threshold (0.0-1.0): ")
                    try:
                        self.conf_thresh = float(new_conf)
                        print(f"Confidence threshold set to {self.conf_thresh}")
                    except:
                        print("Invalid input")

                # Auto-save only if detection is stable
                if bigbox and is_stable:
                    self.save_detection(frame, bigbox)

        self.cap.release()
        cv2.destroyAllWindows()
        print("Detection stopped")

    def save_to_json(self, data):
        os.makedirs('results/text_detect', exist_ok = True)
        with open("results/text_detect/output.json", "w", encoding ="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


app = MedicineApp(model_instance=model, capture_instance=cap)

def process_pipe():
    if precaution():
        app.start_detection()
    else:
        exit()