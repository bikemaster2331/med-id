from paddleocr import PaddleOCR
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

class MedicineApp:
    def ask(self):
        self.name = input("Name: ")
        self.age = input("Age: ")
        self.image = cv2.imread('res/meds/image.png')
        if self.image is None:
            print("Error: Image not found")
            return False
        return True

    def text_extract(self):
        ocr = PaddleOCR(
            use_doc_orientation_classify=False, 
            use_doc_unwarping=False, 
            use_textline_orientation=False) 
        result = ocr.predict(self.image)
        for res in result:
            print(self.name)
            print(self.age)
            res.print()
            # res.save_to_img("output")
            # res.save_to_json("output")

app = MedicineApp()
def process_pipeline():
    if precaution():
        app.ask()
        app.text_extract()
    else:
        exit()
def main():
    process_pipeline()

    
main()

