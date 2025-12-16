import spacy

# Load the new model
try:
    nlp = spacy.load("model/model-best")
    print("✅ Model loaded successfully.")
except OSError:
    print("❌ Model not found. Check the path.")
    exit()

# The Ultimate Test: Unseen drugs, Tricky formatting, and Hard Negatives
test_sentences = [
    # 1. UNSEEN DRUGS (From your Dev list)
    "Prescription for Tramadol 50mg capsule",
    "Take Albuterol 2.5mg now",
    
    # 2. HARD NEGATIVES (Should output NOTHING)
    "Pharmacy: CVS Store #123",
    "Date Filled: 10/12/2023",
    "Qty: 30 Refills: 0",
    "Dr. Smith Signature",
    
    # 3. TRICKY FORMATTING (Real world noise)
    "Rx: ATORVASTATIN 20 MG TAB",   # All caps
    "METFORMIN500mg",               # No space (Common OCR error)
    "Lisinopril 10mg",              # Missing form
]

print(f"\n{'TEXT':<40} | {'ENTITIES'}")
print("-" * 70)

for text in test_sentences:
    doc = nlp(text)
    ents = [(e.text, e.label_) for e in doc.ents]
    print(f"{text:<40} | {ents}")