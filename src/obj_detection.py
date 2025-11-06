import cv2
from ultralytics import YOLO
import sys
import os
import time
from collections import deque
import numpy as np
import json
from paddleocr import PaddleOCR

# --- Configuration Constants (Project-wide settings) ---
CONF_THRESHOLD = 0.75 
CONF_THRESHOLD_IMAGE = 0.60  
MIN_DETECTION_AREA = 5000  
MIN_DETECTION_AREA_IMAGE = 2000  
STABILITY_FRAMES = 5 
COOLDOWN_SECONDS = 3  
MODEL_PATH = "ai/runs/detect/train5/weights/best.pt"
SAVE_DIR = "output"

# --- Global Components (Loaded once) ---
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"ERROR: Could not load YOLO model at {MODEL_PATH}. {e}")
    sys.exit()

# Note: We keep cap here, but handle opening failures in the class.
cap = cv2.VideoCapture(0) 
os.makedirs(SAVE_DIR, exist_ok=True)


# --- Precaution Function (Startup) ---
def precaution():
    print("\n--- SAFETY WARNING ---")
    print("This app provides general information about medicines. \nWe are not medical professionals, and this does not replace professional advice. \nAlways consult a healthcare provider before taking any medicine.\nBy using this app, you agree to use it at your own risk.")

    while True:
        choice = input("Do you want to continue? (Y/N): ").lower()
        if choice == "y":
            print("Welcome to Med-ID, starting camera stream...")
            return True
        elif choice == "n":
            print("Exiting...")
            return False
        else:
            print("Invalid choice. Please enter Y or N.")

# --- Main Application Class ---
class MedicineApp:

    def __init__(self, model_instance, capture_instance):
        self.model = model_instance
        self.cap = capture_instance
        self.save_dir = SAVE_DIR
        self.history = deque(maxlen=STABILITY_FRAMES)
        
        self.last_save_time = 0
        self.last_class_detected = None
        
        self.conf_thresh = CONF_THRESHOLD
        self.min_area = MIN_DETECTION_AREA
        self.cooldown = COOLDOWN_SECONDS
        
        # --- CRITICAL FIX: OCR Initialization ---
        try:
            # Initialize OCR once when the app starts
            self.ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False) 
        except Exception as e:
            print(f"ERROR: Could not initialize PaddleOCR. Ensure installation is correct. {e}")
            sys.exit()

    # --- Utility Methods (IOU, Stability, NMS) ---

    def calculate_iou(self, box1, box2):
        """Calculate Intersection over Union between two boxes"""
        x1_1, y1_1, x2_1, y2_1 = box1
        x1_2, y1_2, x2_2, y2_2 = box2
        
        x_left = max(x1_1, x1_2)
        y_top = max(y1_1, y1_2)
        x_right = min(x2_1, x2_2)
        y_bottom = min(y2_1, y2_2)
        
        if x_right < x_left or y_bottom < y_top:
            return 0.0
        
        intersection_area = (x_right - x_left) * (y_bottom - y_top)
        box1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
        box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
        union_area = box1_area + box2_area - intersection_area
        
        return intersection_area / union_area if union_area > 0 else 0

    def is_stable_detection(self, current_box, history, iou_threshold=0.6):
        """Check if detection is stable across frames"""
        if len(history) < STABILITY_FRAMES:
            return False

        classes = [h[4] for h in history]
        if len(set(classes)) > 1:
            return False

        for prev_box in history:
            if self.calculate_iou(current_box[:4], prev_box[:4]) < iou_threshold:
                return False

        return True

    def apply_nms_custom(self, boxes, iou_threshold=0.5):
        """Apply Non-Maximum Suppression to remove overlapping boxes"""
        if len(boxes) == 0:
            return []

        boxes = sorted(boxes, key=lambda x: x[5], reverse=True)

        keep = []
        while len(boxes) > 0:
            keep.append(boxes[0])
            boxes = [box for box in boxes[1:]
                    if self.calculate_iou(keep[-1][:4], box[:4]) < iou_threshold]

        return keep

    # --- OCR Integration Methods ---

    def text_extract(self, cropped_image):
        """
        Runs PaddleOCR on the cropped image (medicine bottle) to extract text 
        and saves the result to a JSON file.
        """
        # CRITICAL FIX: Use self.ocr instance and the provided cropped_image parameter
        result = self.ocr.ocr(cropped_image, cls=True) 
        extracted_text_list = []

        if result and result[0]:
            for line in result[0]:
                text, confidence = line[1] 
                
                if confidence > 0.75:
                    extracted_text_list.append({
                        "text": text,
                        "confidence": confidence
                    })
        
        if not extracted_text_list:
            print("[OCR] No text found above threshold 0.75")
        
        self.save_to_json(extracted_text_list)
        return extracted_text_list

    def save_to_json(self, data):
        os.makedirs('results/text_detect', exist_ok=True)
        timestamp = int(time.time())
        filepath = os.path.join("results/text_detect", f"ocr_output_{timestamp}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"[OCR] Saved output to {filepath}")


    # --- Core Processing Methods ---

    def run_model(self, frame, debug_mode=False, use_image_thresholds=False):
        
        conf_thresh = CONF_THRESHOLD_IMAGE if use_image_thresholds else self.conf_thresh
        area_thresh = MIN_DETECTION_AREA_IMAGE if use_image_thresholds else self.min_area

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
                
                if conf <= conf_thresh:
                    rejection_reason = f"Low confidence: {conf:.3f} <= {conf_thresh}"
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

        filtered_detections = self.apply_nms_custom(all_detections)

        # Find the largest detection (bigbox) and draw stability info
        bigbox = None
        max_area = 0
        
        for detection in filtered_detections:
            x1, y1, x2, y2, cls, conf = detection
            area = (x2 - x1) * (y2 - y1)
            if area > max_area:
                max_area = area
                bigbox = detection

        # Drawing logic (unchanged)
        for detection in filtered_detections:
            x1, y1, x2, y2, cls, conf = detection
            color = (0, 255, 0) if detection == bigbox else (255, 0, 0)
            thickness = 2 if detection == bigbox else 1
            label = f"{self.model.names[cls]} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Stability check
        is_stable = False
        if bigbox:
            self.history.append(bigbox)
            is_stable = self.is_stable_detection(bigbox, self.history)

            if is_stable:
                cv2.putText(frame, "STABLE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                remaining = STABILITY_FRAMES - len(self.history)
                cv2.putText(frame, f"Stabilizing... {remaining}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
        else:
            self.history.clear()

        cv2.putText(frame, f"Conf: {self.conf_thresh:.2f} | Area: {self.min_area}", 
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow("YOLO Detection", frame)

        return bigbox, is_stable

    def save_detection(self, frame, bigbox, bypass_cooldown=False):
        """Save detection with cooldown and perform OCR."""
        
        current_time = time.time()
        x1, y1, x2, y2, cls, conf = bigbox

        if not bypass_cooldown and current_time - self.last_save_time < self.cooldown:
            print(f"Cooldown active. Wait {self.cooldown - (current_time - self.last_save_time):.1f}s")
            return False

        # --- 1. Crop Image ---
        padding = 20
        h, w = frame.shape[:2]
        y1_pad = max(0, y1 - padding)
        y2_pad = min(h, y2 + padding)
        x1_pad = max(0, x1 - padding)
        x2_pad = min(w, x2 + padding) 
        
        # This is the image used for OCR and saving
        cropped_image = frame[y1_pad:y2_pad, x1_pad:x2_pad]

        # --- 2. Perform OCR (Integrated Pipeline Step) ---
        extracted_text = self.text_extract(cropped_image)
        print(f"[OCR] Extracted {len(extracted_text)} text lines.")

        # --- 3. Save Cropped Image ---
        class_name = self.model.names[cls]
        filename = f"{class_name}_{int(current_time)}_conf{conf:.2f}.jpg"
        filepath = os.path.join(self.save_dir, filename)
        cv2.imwrite(filepath, cropped_image)

        self.last_save_time = current_time
        self.last_class_detected = cls
        print(f"✅ Saved: {filename}")
        return True

    def start_detection(self):
        """The main execution loop for the video stream."""
        
        is_camera_open = self.cap.isOpened()
        
        print("Starting detection loop...")
        print(f"Settings: Confidence={self.conf_thresh:.2f}, MinArea={self.min_area}, Stability={STABILITY_FRAMES} frames")
        print("Press 'q' to quit, 's' to force save, 'c' to adjust confidence")

        while True:
            frame = None 
            ret = False
            
            # --- CAMERA READ ---
            if is_camera_open:
                ret, frame = self.cap.read()
            
            # --- CAMERA FAILURE / IMAGE UPLOAD FALLBACK ---
            if not ret:
                print("\n❌ Camera not detected or stream failed.")
                ans = input("Upload image instead? (Y/N): ").strip().lower()

                if ans == "n":
                    print("Exiting...")
                    self.cap.release()
                    cv2.destroyAllWindows()
                    sys.exit()
                elif ans == "y":
                    image_path = input("Enter image path: ").strip()
                    frame = cv2.imread(image_path) 

                    if frame is None:
                        print("❌ Image not found. Trying again.")
                        continue # Loop back to ask for input again
                    else:
                        bigbox, is_stable = self.run_model(frame, debug_mode=True, use_image_thresholds=True)
                        if bigbox:
                            print(f"📸 Static image mode - saving without stability check")
                            # CRITICAL FIX: Call save_detection with the correct frame data
                            self.save_detection(frame, bigbox, bypass_cooldown=True) 
                        else:
                            print("❌ No valid detections found")
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        sys.exit() # Exit after processing static image
            
            # --- LIVE VIDEO STREAM LOGIC ---
            else:
                bigbox, is_stable = self.run_model(frame)

                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break
                elif key == ord("s") and bigbox:
                    self.save_detection(frame, bigbox, bypass_cooldown=True) 
                elif key == ord("c"):
                    new_conf = input("Enter new confidence threshold (0.0-1.0): ")
                    try:
                        self.conf_thresh = float(new_conf)
                        print(f"Confidence threshold set to {self.conf_thresh}")
                    except:
                        print("Invalid input")

                # Auto-save only if detection is stable (OCR and save triggered here)
                if bigbox and is_stable:
                    self.save_detection(frame, bigbox)

        self.cap.release()
        cv2.destroyAllWindows()
        print("Detection stopped")



if precaution():
    # Instantiate the class, passing the global model and cap objects
    app = MedicineApp(model_instance=model, capture_instance=cap)
    app.start_detection()