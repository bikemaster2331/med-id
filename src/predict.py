import spacy
import json
import os
import sys

# Load your trained model
try:
    # Make sure this points to your actual model folder
    nlp = spacy.load("model/model-best") 
except Exception as e:
    print(f"❌ Error loading model: {e}")
    sys.exit(1)

# Load the OCR output
try:
    with open("results/text_detect/output.json", "r", encoding="utf-8") as f:
        raw_ocr_data = json.load(f)
except FileNotFoundError:
    print("❌ OCR output file not found.")
    sys.exit(1)

# === 🛑 THE BLOCKLIST ===
# Words that the model might mistake for drugs, but definitely aren't.
BLOCKLIST = {
    "PHARMACY", "RX", "DATE", "FILLED", "QTY", "REFILL", "TAKE", "TABLET", 
    "CAPSULE", "EVERY", "DAY", "ONCE", "TWICE", "DAILY", "ORAL", "MOUTH",
    "CHEN", "PFIZER", "NOVARTIS", "GSK", "MERCK", "SANOFI", 
    "MFG", "INC", "LTD", "CO", "PHARMA", "LABS", "PHARMACEUTICALS",
    "BAYER", "ROCHE", "ASTRAZENECA", "JOHNSON", "BRISTOL", "Prescription"
}

def filter_and_score(doc):
    """
    Analyzes the entities in a doc and assigns a 'quality score'.
    Returns: (score, clean_drug_name)
    """
    has_drug = False
    has_dosage = False
    drug_text = None
    
    entities_found = []
    
    for ent in doc.ents:
        label = ent.label_
        text = ent.text.strip()
        entities_found.append({"text": text, "label": label})
        
        # Check for Drug Name
        if label == "DRUG_NAME":
            # 1. Check Blocklist (Case insensitive)
            if text.upper() in BLOCKLIST:
                continue # Skip this, it's a bad prediction (like "Pharmacy")
            
            # 2. Check length (Drugs are usually > 3 chars)
            if len(text) < 3:
                continue

            if any(text.upper().endswith(suffix) for suffix in ["INC", "LTD", "CO", "LABS"]):
                continue
                
            has_drug = True
            drug_text = text
            
        # Check for Dosage
        if label == "DOSAGE":
            has_dosage = True

    # === SCORING LOGIC ===
    score = 0
    
    if has_drug and has_dosage:
        score = 3  # Gold Standard: We found a drug AND a strength (e.g. Lisinopril 5mg)
    elif has_drug:
        score = 1  # Medium: We found a drug name, but no strength (e.g. Doliprane)
    else:
        score = 0  # Garbage: Only found "Filled" or "Pharmacy" or nothing
        
    return score, drug_text, entities_found

# ==========================================
# MAIN PROCESSING LOOP
# ==========================================

best_candidate = None
highest_score = -1
all_results = []

print(f"{'ORIGINAL TEXT':<30} | {'SCORE'} | {'ENTITIES'}")
print("-" * 70)

for item in raw_ocr_data:
    original_text = item['text']
    
    # Run the model
    doc = nlp(original_text)
    
    # Apply our filter logic
    score, drug_name, entities = filter_and_score(doc)
    
    # Log for debugging
    print(f"{original_text[:30]:<30} | {score:<5} | {entities}")
    
    # Keep track of the best result found so far
    if score > highest_score and score > 0:
        highest_score = score
        best_candidate = {
            "original_text": original_text,
            "drug_name": drug_name,
            "entities": entities
        }

# ==========================================
# SAVE FINAL RESULT
# ==========================================

final_output = []

if best_candidate:
    print("\n✅ BEST MATCH FOUND:")
    print(f"   Drug: {best_candidate['drug_name']}")
    print(f"   Source Line: {best_candidate['original_text']}")
    
    # Format for your next step (FDA API)
    final_output.append({
        "text": best_candidate['drug_name'],
        "confidence": 1.0 # We set this to 1.0 because our NER logic validated it
    })
else:
    print("\n❌ No valid medicine detected.")

# Save to the filter file
os.makedirs('results/filter', exist_ok=True)
with open("results/filter/output_next.json", "w", encoding="utf-8") as f:
    json.dump(final_output, f, ensure_ascii=False, indent=4)

print("✓ Results saved to results/filter/output_next.json")