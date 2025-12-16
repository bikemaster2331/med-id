import random
import json
import os
import re
from typing import List, Tuple

os.makedirs("data", exist_ok=True)

# === EXPANDED DATA LISTS ===
ALL_DRUGS = [
    "Lisinopril", "Paracetamol", "Acetaminophen", "Ibuprofen", "Amoxicillin",
    "Metformin", "Atorvastatin", "Amlodipine", "Omeprazole", "Azithromycin",
    "Ciprofloxacin", "Cetirizine", "Loratadine", "Prednisone", "Ondansetron",
    "Simvastatin", "Losartan", "Hydroxyzine", "Doxycycline", "Clopidogrel",
    "Fluconazole", "Gabapentin", "Metoprolol", "Levothyroxine", "Alprazolam",
    "Tramadol", "Clonazepam", "Escitalopram", "Furosemide", "Trazodone",
    "Albuterol", "Pantoprazole", "Montelukast", "Fluticasone", "Sertraline",
    "Rosuvastatin", "Aspirin", "Meloxicam", "Duloxetine", "Tamsulosin",
    "Spironolactone", "Clindamycin", "Diclofenac", "Atenolol", "Naproxen",
    "Methylprednisolone", "Finasteride", "Sitagliptin", "Celecoxib", "Donepezil",
    "Oxycodone", "Hydromorphone", "Warfarin", "Apixaban", "Rivaroxaban",
    "Insulin", "Glipizide", "Famotidine", "Hydrochlorothiazide", "Triamcinolone",
    "Lovastatin", "Pravastatin", "Mirtazapine", "Risperidone", "Quetiapine",
    "Olanzapine", "Aripiprazole", "Lamotrigine", "Topiramate", "Pregabalin"
]

CORRUPTED_DRUGS = [
    "Paratecamol", "Metforrmin", "Omepprazole", "Lisinorpil",
    "Atorvasttin", "Gabapentln", "Metroprolol", "Ibuprofin"
]

MANUFACTURERS = [
    "Chen", "Pfizer", "Novartis", "GSK", "Merck", "Sanofi", "Bayer", "Roche", 
    "AstraZeneca", "Johnson", "Bristol", "Teva", "Sandoz", "Mylan", "Sun", 
    "Lupin", "Aurobindo", "Cipla", "Hikma", "Amneal", "Glenmark", "Zydus",
    "Torrent", "AbbVie", "Gilead", "Amgen", "Lilly", "Nordisk", "Boehringer",
    "Takeda", "Viatris", "Organon", "Perrigo", "Apotex", "Bausch", "Biocon"
]

# === CRITICAL: Label Header Words ===
LABEL_HEADERS = [
    "Pharmacy", "Store", "Clinic", "Hospital", "Center", "Rx", "Date", 
    "Filled", "Refill", "Qty", "Quantity", "Doctor", "Patient", "Name",
    "Address", "Phone", "Fax", "Tel", "Prescription", "Order", "Number",
    "Discard", "Expiry", "Batch", "Lot", "NDC", "DIN", "License",
    "Directions", "Instructions", "Dosage", "Take", "Use", "Warning",
    "Caution", "Storage", "Keep", "Contains", "Active", "Inactive",
    "Ingredient", "Manufactured", "Distributed", "Packaged", "By"
]

# === Common Pharmacy/Store Names (NOT DRUGS!) ===
PHARMACY_NAMES = [
    "CVS", "Walgreens", "Rite Aid", "Walmart", "Target", "Kroger",
    "Safeway", "Publix", "Costco", "Sam's Club", "Albertsons", "HEB",
    "Duane Reade", "Health Mart", "Good Neighbor", "Medicine Shoppe"
]

# === Common Words That Look Like Drugs (NOT DRUGS!) ===
DECEPTIVE_WORDS = [
    "Store", "Health", "Care", "Medical", "Wellness", "Family", 
    "Community", "Express", "Plus", "Prime", "Central", "Main",
    "Street", "Avenue", "Plaza", "Mall", "Building", "Suite",
    "North", "South", "East", "West", "City", "Town", "Village"
]

DOSAGES = [
    "5 mg", "10 mg", "25 mg", "50 mg", "100 mg", "250 mg", "500 mg",
    "5mg", "10mg", "25mg", "50mg", "100mg", "200mg", "500mg",
    "2.5 mg", "1 g", "0.5 mg", "0.25 mg", "1000 mg", "600 mg",
    "40 mg", "20 mg", "150 mg", "75 mg", "12.5 mg", "81 mg",
    "50 mcg", "100 mcg", "200 mcg", "5 ml", "10 ml", "100 ml"
]

FORMS = [
    "tablet", "tablets", "tab", "tabs", "capsule", "capsules", "caps",
    "syrup", "ointment", "cream", "injection", "drops", "caplet",
    "pill", "pills", "suspension", "solution", "liquid", "gel"
]

STRENGTHS = ["ER", "XR", "SR", "Forte", "IR", "CR", "DR", "LA", "XL"]


class LabeledToken:
    def __init__(self, text: str, label: str = None, spacing: str = " "):
        self.text = text
        self.label = label
        self.spacing = spacing


def build_positive_sentence(allowed_drugs: List[str]) -> List[LabeledToken]:
    """Builds sentences with ACTUAL drug names"""
    sentence = []
    drug = random.choice(allowed_drugs)
    dosage = random.choice(DOSAGES) if random.random() < 0.85 else None
    form = random.choice(FORMS) if random.random() < 0.85 else None
    strength = random.choice(STRENGTHS) if random.random() < 0.25 else None
    
    pattern = random.choice([
        "basic", "with_rx", "with_take", "with_continue", 
        "with_parentheses", "with_for", "with_header"  # NEW
    ])
    
    if pattern == "with_rx":
        sentence.append(LabeledToken("Rx:", None, spacing=""))
    elif pattern == "with_take":
        sentence.append(LabeledToken("Take", None, spacing=" "))
    elif pattern == "with_continue":
        sentence.append(LabeledToken("Continue", None, spacing=" "))
    elif pattern == "with_for":
        sentence.append(LabeledToken("For:", None, spacing=" "))
    elif pattern == "with_header":
        # CRITICAL: Teach model that drugs CAN appear after headers!
        # "Pharmacy: Amoxicillin 500mg" or "Prescription: Lisinopril"
        header = random.choice(["Pharmacy", "Prescription", "Rx", "Medication", "Drug"])
        sentence.append(LabeledToken(header, None, spacing=""))
        sentence.append(LabeledToken(":", None, spacing=" "))
    
    sentence.append(LabeledToken(drug, "DRUG_NAME", spacing=" "))
    
    if pattern == "with_parentheses" and dosage:
        sentence.append(LabeledToken("(", None, spacing=""))
        sentence.append(LabeledToken(dosage, "DOSAGE", spacing=""))
        sentence.append(LabeledToken(")", None, spacing=" "))
    else:
        if dosage:
            sentence.append(LabeledToken(dosage, "DOSAGE", spacing=" "))
    
    if strength and pattern != "with_parentheses":
        sentence.append(LabeledToken(strength, "STRENGTH", spacing=" "))
    
    if form:
        sentence.append(LabeledToken(form, "FORM", spacing=" "))
    
    if sentence:
        sentence[-1].spacing = ""
    
    return sentence


def build_negative_sentence() -> List[LabeledToken]:
    """
    CRITICAL: Builds sentences that LOOK like drugs but ARE NOT.
    This teaches the model context, not just capitalized words.
    """
    pattern = random.choice([
        "pharmacy_label",    # "Pharmacy: CVS"
        "store_label",       # "Store #1234"
        "header_colon",      # "Patient: John Doe"
        "manufacturer",      # "Pfizer Pharmaceuticals"
        "deceptive_caps",    # "Health Center" (looks like drug!)
        "corrupted",         # "Paratecamol" (typo)
        "instruction",       # "Take with food"
        "mixed_noise"        # "Store #5 - Pharmacy"
    ])
    
    sentence = []
    
    if pattern == "pharmacy_label":
        # "Pharmacy: CVS" or "Pharmacy: Walgreens Store #123"
        sentence.append(LabeledToken("Pharmacy", None, ""))
        sentence.append(LabeledToken(":", None, " "))
        
        pharm = random.choice(PHARMACY_NAMES)
        sentence.append(LabeledToken(pharm, None, " "))
        
        # Sometimes add store number
        if random.random() < 0.5:
            sentence.append(LabeledToken("Store", None, " "))
            sentence.append(LabeledToken("#", None, ""))
            sentence.append(LabeledToken(str(random.randint(100, 9999)), None, ""))
    
    elif pattern == "store_label":
        # "Store #1234" or "Store: Main Street"
        sentence.append(LabeledToken("Store", None, " "))
        
        if random.random() < 0.7:
            sentence.append(LabeledToken("#", None, ""))
            sentence.append(LabeledToken(str(random.randint(1, 9999)), None, ""))
        else:
            sentence.append(LabeledToken(":", None, " "))
            loc = random.choice(["Main St", "Central Ave", "Plaza", "Mall"])
            sentence.append(LabeledToken(loc, None, ""))
    
    elif pattern == "header_colon":
        # "Patient: John Doe" or "Doctor: Smith"
        header = random.choice(LABEL_HEADERS)
        sentence.append(LabeledToken(header, None, ""))
        sentence.append(LabeledToken(":", None, " "))
        
        # Add realistic value
        if "Date" in header or "Expiry" in header:
            val = f"{random.randint(1,12)}/{random.randint(1,28)}/{random.randint(2023,2026)}"
        elif "Phone" in header or "Fax" in header:
            val = f"555-{random.randint(1000,9999)}"
        elif "Qty" in header or "Refill" in header:
            val = str(random.randint(0, 99))
        else:
            # Names
            val = random.choice(["John Doe", "Smith", "Johnson", "CVS", "Walgreens"])
        
        sentence.append(LabeledToken(val, None, ""))
    
    elif pattern == "manufacturer":
        # "Pfizer Pharmaceuticals" or "GSK Labs Inc"
        mfg = random.choice(MANUFACTURERS)
        sentence.append(LabeledToken(mfg, None, " "))
        
        if random.random() < 0.6:
            suffix = random.choice(["Pharmaceuticals", "Labs", "Inc", "Co", "Ltd", "LLC"])
            sentence.append(LabeledToken(suffix, None, ""))
    
    elif pattern == "deceptive_caps":
        # "Health Center" or "Medical Plaza" - Capitalized but NOT drugs!
        word1 = random.choice(DECEPTIVE_WORDS)
        word2 = random.choice(DECEPTIVE_WORDS)
        
        sentence.append(LabeledToken(word1, None, " "))
        sentence.append(LabeledToken(word2, None, ""))
    
    elif pattern == "corrupted":
        # Misspelled drug names (NOT real drugs)
        fake_drug = random.choice(CORRUPTED_DRUGS)
        sentence.append(LabeledToken(fake_drug, None, " "))
        
        # Sometimes add dosage to make it MORE deceptive
        if random.random() < 0.5:
            sentence.append(LabeledToken(random.choice(["50mg", "100mg", "25mg"]), None, ""))
    
    elif pattern == "instruction":
        # "Take with food" or "Use as directed"
        instructions = [
            ["Take", "with", "food"],
            ["Use", "as", "directed"],
            ["Keep", "refrigerated"],
            ["Shake", "well"],
            ["Do", "not", "crush"],
            ["For", "external", "use"],
            ["Swallow", "whole"]
        ]
        
        inst = random.choice(instructions)
        for i, word in enumerate(inst):
            spacing = " " if i < len(inst) - 1 else ""
            sentence.append(LabeledToken(word, None, spacing))
    
    elif pattern == "mixed_noise":
        # "Store #5 - Pharmacy CVS" (complex multi-word non-drug)
        sentence.append(LabeledToken("Store", None, " "))
        sentence.append(LabeledToken("#", None, ""))
        sentence.append(LabeledToken(str(random.randint(1, 99)), None, " "))
        sentence.append(LabeledToken("-", None, " "))
        sentence.append(LabeledToken("Pharmacy", None, " "))
        sentence.append(LabeledToken(random.choice(PHARMACY_NAMES), None, ""))
    
    return sentence


def apply_noise_to_sentence(sentence: List[LabeledToken]) -> List[LabeledToken]:
    """Apply realistic OCR-style noise"""
    noisy_sentence = []
    for token in sentence:
        if token.label is not None:
            # Don't corrupt labeled entities
            noisy_sentence.append(LabeledToken(token.text, token.label, token.spacing))
        else:
            rand = random.random()
            if rand < 0.15:
                # ALL CAPS (common in labels)
                noisy_sentence.append(LabeledToken(token.text.upper(), None, token.spacing))
            elif rand < 0.30:
                # lowercase
                noisy_sentence.append(LabeledToken(token.text.lower(), None, token.spacing))
            else:
                # Keep original
                noisy_sentence.append(LabeledToken(token.text, None, token.spacing))
    return noisy_sentence


def sentence_to_text_and_entities(sentence: List[LabeledToken]) -> Tuple[str, List]:
    """Convert tokens to text + entity spans"""
    text_parts = []
    entities = []
    current_pos = 0
    
    for token in sentence:
        token_start = current_pos
        text_parts.append(token.text)
        token_end = current_pos + len(token.text)
        
        if token.label is not None:
            entities.append([token_start, token_end, token.label])
        
        current_pos = token_end
        
        if token.spacing:
            text_parts.append(token.spacing)
            current_pos += len(token.spacing)
    
    return "".join(text_parts), entities


def generate_batch(drug_list, n_count, neg_ratio=0.4):
    """
    Generate balanced training data.
    INCREASED neg_ratio to 0.4 (40%) to ensure model sees LOTS of non-drug examples.
    """
    batch = []
    target_neg = int(n_count * neg_ratio)
    
    # Generate Negatives (MORE important for edge cases!)
    for _ in range(target_neg):
        sent = build_negative_sentence()
        sent = apply_noise_to_sentence(sent)
        txt, ents = sentence_to_text_and_entities(sent)
        batch.append((txt, {"entities": ents}))
    
    # Generate Positives
    for _ in range(n_count - target_neg):
        sent = build_positive_sentence(drug_list)
        sent = apply_noise_to_sentence(sent)
        txt, ents = sentence_to_text_and_entities(sent)
        batch.append((txt, {"entities": ents}))
    
    random.shuffle(batch)
    return batch


if __name__ == "__main__":
    random.seed(42)
    
    # Split drugs: 80% Training, 20% Dev
    random.shuffle(ALL_DRUGS)
    split_idx = int(len(ALL_DRUGS) * 0.8)
    train_drug_list = ALL_DRUGS[:split_idx]
    dev_drug_list = ALL_DRUGS[split_idx:]
    
    print(f"📊 Training Drugs ({len(train_drug_list)}): {train_drug_list[:5]}...")
    print(f"📊 Unseen Dev Drugs ({len(dev_drug_list)}): {dev_drug_list}")
    
    # Generate MORE data with MORE negative examples
    train_data = generate_batch(train_drug_list, n_count=3000)  # Increased from 2000
    dev_data = generate_batch(dev_drug_list, n_count=600)      # Increased from 400
    
    with open("data/train_spacy.json", "w", encoding="utf-8") as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)
    
    with open("data/dev_spacy.json", "w", encoding="utf-8") as f:
        json.dump(dev_data, f, ensure_ascii=False, indent=2)
    
    # Show examples of what was generated
    print(f"\n✅ Generated {len(train_data)} training samples and {len(dev_data)} dev samples.")
    print("\n📝 Sample Negative Examples (what the model learns to IGNORE):")
    
    neg_samples = [item for item in train_data if len(item[1]["entities"]) == 0][:5]
    for text, _ in neg_samples:
        print(f"   ❌ '{text}'")
    
    print("\n📝 Sample Positive Examples (what the model learns to DETECT):")
    pos_samples = [item for item in train_data if len(item[1]["entities"]) > 0][:5]
    for text, annot in pos_samples:
        entities_str = ", ".join([f"{text[e[0]:e[1]]}({e[2]})" for e in annot["entities"]])
        print(f"   ✅ '{text}' → [{entities_str}]")