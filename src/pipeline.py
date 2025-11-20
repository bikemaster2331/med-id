from paddleocr import PaddleOCR
import json
import cv2
import os
import time

class MedicineApp:
    def __init__(self):
        self.ocr = PaddleOCR(use_textline_orientation=True, lang='en')
        self.current_image = None
        self.save_dir = "output"
        os.makedirs(self.save_dir, exist_ok=True)
    
    def precaution(self):
        """Show medical disclaimer"""
        print("\n⚠️  MEDICAL DISCLAIMER")
        print("-" * 70)
        print("This app provides general information about medicines.")
        print("We are not medical professionals, and this does not replace professional advice.")
        print("Always consult a healthcare provider before taking any medicine.")
        print("By using this app, you agree to use it at your own risk.")
        print("-" * 70)
        
        while True:
            choice = input("\nDo you want to continue? (Y/N): ").strip().lower()
            if choice == "y":
                print("✅ Welcome to Med-ID!\n")
                return True
            elif choice == "n":
                print("👋 Exiting...")
                exit()
            else:
                print("❌ Invalid input. Please enter Y or N.")

    def load_image(self, image_path):
        """Load image from file path"""
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"❌ Image not found: {image_path}")
            return None
        
        print(f"✅ Image loaded: {image_path}")
        self.current_image = image
        return image
    
    def cam_capture(self):
        """Capture image from camera - Press SPACE to capture, Q to quit"""
        cap = cv2.VideoCapture(0)
            
        
        print("\n🎥 Camera active")
        print("📸 Press SPACE to capture image")
        print("🚪 Press Q to quit")
        
        while True:
            ret, frame = cap.read()
            
            if not ret and not cap.isOpened():
                print("❌ Failed to read from camera")
                option = input("\nDo you want to upload a picture instead? (Y/N): ").strip().lower()

                if option == "y":
                    image_path = input("📁 Enter image path: ").strip()
                    return self.load_image(image_path)
                elif option == "n":
                    exit()
                else:
                    print("Invalid input")
            
            # Show live feed
            cv2.imshow("Med-ID Camera - Press SPACE to capture", frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):  # Space key - capture
                # Save captured image
                timestamp = int(time.time())
                filename = f"captured_{timestamp}.jpg"
                filepath = os.path.join(self.save_dir, filename)
                cv2.imwrite(filepath, frame)
                
                print(f"✅ Image captured: {filename}")
                self.current_image = frame
                
                cap.release()
                cv2.destroyAllWindows()
                return frame
            
            elif key == ord('q'):  # Q key - quit
                print("❌ Capture cancelled")
                cap.release()
                cv2.destroyAllWindows()
                return None
    
    def mode(self):
        """Let user choose between camera or upload"""
        print("\n" + "=" * 70)
        print("📷 Choose Input Method")
        print("=" * 70)
        print("1. Camera (capture photo)")
        print("2. Upload image")
        
        while True:
            choice = input("\nEnter choice (1/2): ").strip()
            
            if choice == "1":
                return self.cam_capture()
            elif choice == "2":
                image_path = input("📁 Enter image path: ").strip()
                return self.load_image(image_path)
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")
    
    def text_extract(self, image=None):
        """Extract text from image using OCR"""
        if image is None:
            image = self.current_image

        if image is None:
            print("❌ No image available for OCR")
            return []

        print("\n" + "=" * 70)
        print("🔍 Extracting text from medicine label...")
        print("=" * 70)

        # Run OCR using predict()
        try:
            result = self.ocr.predict(image)
        except Exception as e:
            print(f"❌ OCR failed: {e}")
            return []

        extracted_text = []

        # Parse predict() results - different structure
        if result and len(result) > 0:
            result_dict = result[0]

            # Check if keys exist
            if 'rec_texts' in result_dict and 'rec_scores' in result_dict:
                texts = result_dict['rec_texts']
                scores = result_dict['rec_scores']

                for text, confidence in zip(texts, scores):
                    if confidence > 0.8:
                        extracted_text.append({
                            "text": text,
                            "confidence": float(confidence)
                        })
                        print(f"  📄 {text} (confidence: {confidence:.2f})")
            else:
                print("❌ Unexpected OCR result format")

        if not extracted_text:
            print("❌ No text found in image")
        else:
            print(f"\n✅ Successfully extracted {len(extracted_text)} text entries!")

        self.save_to_json(extracted_text)
        
        return extracted_text
    
    def save_to_json(self, data):
        """Save OCR results to JSON"""
        os.makedirs('results/text_detect', exist_ok=True)
        filepath = "results/text_detect/output.json"
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"💾 Results saved to: {filepath}")
    
    def run(self):
        """Main application workflow"""
        print("\n" + "=" * 70)
        print("🏥 Med-ID: Medicine Text Recognition System")
        print("=" * 70)
        
        # Show precaution
        if not self.precaution():
            return
        
        # Get image (camera or upload)
        image = self.mode()
        
        if image is None:
            print("\n❌ No image provided. Exiting...")
            exit()
        
        # Extract text from image
        extracted_text = self.text_extract(image)
        
        if extracted_text:
            print("\n✅ Processing complete!")
        else:
            print("\n⚠️ No text could be extracted from the image")

def process_pipe():
    app = MedicineApp()
    app.run()