import sqlite3
import os 

DB_FILE = 'meds_db.sqlite'

SAMPLES = [
    ("Paracetamol", "MED_NAME"),
    ("Ibuprofen", "MED_NAME"),
    ("Amoxicillin", "MED_NAME"),
    ("Metformin", "MED_NAME"),
    ("Loratadine", "MED_NAME"),
    ("Omeprazole", "MED_NAME"),
    ("Simvastatin", "MED_NAME"),
    ("Azithromycin", "MED_NAME"),
    ("Diclofenac", "MED_NAME"),
    ("Atorvastatin", "MED_NAME"),
    ("Losartan", "MED_NAME"),
    ("Amlodipine", "MED_NAME"),
    ("Clopidogrel", "MED_NAME"),
    ("Hydroxyzine", "MED_NAME"),
    ("Doxycycline", "MED_NAME"),
    ("Prednisone", "MED_NAME"),
    ("Montelukast", "MED_NAME"),    
    ("Xyzmab", "MED_NAME"),
    ("Cardiprene", "MED_NAME"),
    ("Neurozol", "MED_NAME"),
    ("Fluconazole", "MED_NAME"),
    ("Ranitidine", "MED_NAME"),
]

def setup():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY, 
            name TEXT UNIQUE NOT NULL
        )
    ''')

    insert_names = []
    for text, label in SAMPLES:
        if label == "MED_NAME":
            insert_names.append((text.lower(),))

    cursor.executemany('INSERT OR IGNORE INTO medicines (name) VALUES (?)', insert_names)

    conn.commit()
    print(f"Successfully created/updated {DB_FILE} with {len(insert_names)} entries.")

    conn.close()

if __name__ == '__main__':
    setup()