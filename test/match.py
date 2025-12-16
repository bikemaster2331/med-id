# ill be using fuzzymatching and levenshtein distance to match and filter medicine names detected
# connect this to the pipeline.py
import Levenshtein
import sqlite3
import re
import os

DB_FILE = 'meds_db.sqlite'
MAX_TYPO_TOLERANCE = 2

class RuleClassifier:

    def __init__(self, db = DB_FILE):
        self.db_file = db
        if not os.path.exists(self.db_file):
            print("Database file not found. Run the setup script first")

    def execute_query(self, query:  str, params: tuple = ()) -> list:
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_names(self) -> list:
        query = "SELECT name FROM medicines"
        all_names = self.execute_query(query)
        return [name[0] for name in all_names]

    def classify(self, text_list: list) -> list:

        results = []
        db_name = self.get_names()

        for text in text_list:
            cleaned_text = text.strip().lower()
            is_match = False
            standard_name = None
            exact_match = False

            query = "SELECT name FROM medicines WHERE name = ?"
            matches = self.execute_query(query, (cleaned_text,))

            if matches:
                is_match = True
                standard_name = matches[0][0]
                exact_match = True
            else:
                check = re.split(r'\s+|-|\(|\)', cleaned_text)

                max_letter_tolerance = 3

                for word in check:
                    if len(word) <= max_letter_tolerance: continue
                    for dbstring in db_name:
                        distance = Levenshtein.distance(word, dbstring)
                        if distance > 0 and distance <= MAX_TYPO_TOLERANCE:
                            is_match = True
                            standard_name = dbstring
                            exact_match = False
                            break
                    if is_match:
                        break
            confidence = 1.0 if is_match else 0.0

            results.append({
                "text": text,
                "is_medicine": is_match,
                "confidence": confidence,
                "standard_name": standard_name,
                "exact_match": exact_match
            })

        return results
    

if __name__ == '__main__':

    classifier = RuleClassifier()

    ocr_output = [
        "Paracetamol",         
        "Ibuprophen",           
        "Dosage: Take one tablet daily", 
        "Azithromycin 500mg",   
        "Montelukasst",   
        "Doxycyllline", 
        "Batch No. 12345",  
        "Losartannn" 
    ]

    print("process starting")

    results = classifier.classify(ocr_output)

    for r in results:
        flag = "✅ EXACT MATCH" if r['exact_match'] else ("⚠️ FUZZY WARNING" if r['is_medicine'] else "❌ NOT MEDICINE")
        
        print(f"{flag:^18} | '{r['text']:<25}' -> Corrected Name: {r['standard_name']}")

