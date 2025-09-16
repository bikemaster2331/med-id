from paddleocr import PaddleOCR
import json
import os
import cv2


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


class MedicineApp():

    def ask(self):
        self.image = cv2.imread('res/meds/med1.png')
        if self.image is None:
            print("Error: Image not found")
            return False
        return True    
    
    def text_extract(self):
        ocr = PaddleOCR(use_angle_cls=False, lang='en')
        result = ocr.predict(self.image)
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



    def save_to_json(self, data):
        os.makedirs('results/text_detect', exist_ok = True)
        with open("results/text_detect/output.json", "w", encoding ="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

app = MedicineApp()

def process_pipe():
    if precaution():
        if app.ask():
            app.text_extract()
    else:
        exit()

def main():
    process_pipe()

main()