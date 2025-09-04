from paddleocr import PaddleOCR
import cv2
import json
from datetime import datetime
import requests
import os




# Get API key from environment
api_key = os.getenv("OPEN_FDA_KEY")

url = "https://api.fda.gov/drug/label.json"
params = {
    "search": "ibuprofen",   # example drug
    "limit": 1,
    "api_key": api_key
}

response = requests.get(url, params=params)
data = response.json()

if "results" in data:
    result = data["results"][0]
    

    print("Purpose:", result.get("purpose", ["N/A"])[0])
    print("="*100)
    print("Indications and usage:", result.get("indications_and_usage", ["N/A"])[0])
    print("="*100)
    print("Dosage:", result.get("dosage_and_administration", ["N/A"])[0])
else:
    print("No results found")


# def precaution():
#     print("This app provides general information about medicines. \nWe are not medical professionals, and this does not replace professional advice. \nAlways consult a healthcare provider before taking any medicine.\nBy using this app, you agree to use it at your own risk.")

#     while True:
#         choice = input("Do you want to continue? (Y/N): ").lower()
#         if choice == "y":
#             print("Welcome to Med-ID, please continue to the next process.")
#             return True
#         elif choice == "n":
#             print("Exiting..")
#             return False
#         else:
#             print("Not defined")

# class MedicineApp:
#     def ask(self):
#         self.name = input("Name: ")
#         self.age = input("Age: ")
#         self.image = cv2.imread('res/meds/image.png')
#         if self.image is None:
#             print("Error: Image not found")
#             return False
#         return True

#     def text_extract(self):
#         ocr = PaddleOCR(
#             use_doc_orientation_classify=False, 
#             use_doc_unwarping=False, 
#             use_textline_orientation=False
#         ) 
#         result = ocr.predict(self.image)
    
#         # Extract all text from OCR results
#         extracted_text = []
#         full_text_parts = []

#         try:
#             # PaddleOCR returns a list with one dict item
#             if isinstance(result, list) and len(result) > 0:
#                 # Get the first (and likely only) result dictionary
#                 result_dict = result[0]
                
#                 # Check if it's a dictionary with the expected keys
#                 if isinstance(result_dict, dict) and 'rec_texts' in result_dict and 'rec_scores' in result_dict:
#                     texts = result_dict['rec_texts']
#                     scores = result_dict['rec_scores']
                    
#                     print(f"Found {len(texts)} text segments:")
                    
#                     for i, (text, confidence) in enumerate(zip(texts, scores)):
#                         print(f"{i+1}. '{text}' (confidence: {confidence:.3f})")
                        
#                         extracted_text.append({
#                             "text": text,
#                             "confidence": confidence
#                         })
#                         full_text_parts.append(text)
#                 else:
#                     print("Dictionary doesn't have expected keys")
#                     print(f"Available keys: {list(result_dict.keys()) if isinstance(result_dict, dict) else 'Not a dict'}")
#             else:
#                 print("Result is not a list or is empty")
                
#         except Exception as e:
#             print(f"Error processing OCR results: {e}")
#             extracted_text.append({
#                 "text": f"Error: {str(e)}",
#                 "confidence": 0.0
#             })
#             full_text_parts.append(f"Error: {str(e)}")
    
#         # Create JSON structure
#         data = self.create_json_structure(extracted_text, full_text_parts)
    
#         # Print the JSON
#         print("\n" + "="*50)
#         print("STRUCTURED DATA (JSON):")
#         print("="*50)
#         print(json.dumps(data, indent=2))
    
#         # Save to file
#         self.save_to_json(data)
    
#         return data

#     def create_json_structure(self, extracted_text, full_text_parts):
#         # Combine all extracted text
#         full_text = " ".join(full_text_parts)

#         # Create the JSON structure
#         json_data = {
#             "user_info": {
#                 "name": self.name,
#                 "age": int(self.age) if self.age.isdigit() else self.age
#             },
#             "scan_info": {
#                 "timestamp": datetime.now().isoformat(),
#                 "extracted_text": full_text,
#                 "total_detections": len(extracted_text),
#                 "ocr_details": extracted_text
#             },
#             "medicine_info": {
#                 "raw_data": full_text,
#                 # You can add parsing logic here later
#                 "parsed_name": None,
#                 "parsed_dosage": None,
#                 "parsed_ingredients": None
#             }
#         }

#         return json_data
    
#     def save_to_json(self, data):
#         filename = f"medicine_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
#         try:
#             with open(filename, 'w') as f:
#                 json.dump(data, f, indent=2)
#             print(f"\nData saved to: {filename}")
#         except Exception as e:
#             print(f"Error saving JSON: {e}")

# app = MedicineApp()

# def process_pipeline():
#     if precaution():
#         if app.ask():
#             app.text_extract()
#     else:
#         exit()

# def main():
#     process_pipeline()

# main()