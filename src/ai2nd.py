from paddleocr import PaddleOCR
import json
import os

ocr = PaddleOCR(use_angle_cls=False, lang='en')
result = ocr.predict("res/meds/med1.jpg")
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

print(extracted_text)


os.makedirs('results/text_detect', exist_ok = True)
with open("results/text_detect/output.json", "w", encoding ="utf-8") as f:
    json.dump(extracted_text, f, ensure_ascii=False, indent=4)