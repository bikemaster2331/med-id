import spacy
from spacy.tokens import DocBin
import json
import os

def convert(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create a blank English model
    nlp = spacy.blank("en")
    db = DocBin()
    
    count = 0
    
    print(f"Processing {input_path}...")

    for text, annot in data:
        doc = nlp.make_doc(text)
        ents = []
        
        # Add entities
        if "entities" in annot:
            for start, end, label in annot["entities"]:
                # alignment_mode="contract" ensures we snap to valid token boundaries
                span = doc.char_span(start, end, label=label, alignment_mode="contract")
                if span is None:
                    print(f"⚠️ Skipping invalid span in: {text}")
                else:
                    ents.append(span)
        
        try:
            doc.ents = ents
            db.add(doc)
            count += 1
        except Exception as e:
            print(f"Skipping doc due to overlap error: {e}")

    db.to_disk(output_path)
    print(f"✅ Saved {count} documents to {output_path}")

if __name__ == "__main__":
    convert("data/train_spacy.json", "data/train.spacy")
    convert("data/dev_spacy.json", "data/dev.spacy")