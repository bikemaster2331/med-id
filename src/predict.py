import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import json
import os
import sys

with open("results/text_detect/output.json", "r", encoding="utf-8") as f:
    extracted_text = json.load(f)

# Ensure results directory exists
os.makedirs('results/filter', exist_ok=True)

if not extracted_text:
    print("No text found...")
    with open("results/filter/output_next.json", "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)
    sys.exit()

else:
    test_texts = []  # make an empty list first

    for item in extracted_text:
        if item.get("text", "").strip():  # check if "text" exists and not empty
            text = item["text"].strip()   # get the text and remove spaces
            test_texts.append(text)        # add it to the list

if not test_texts:
    print("No valid text found after filtering empty strings. Creating empty output file...")
    # Write empty array to JSON file
    with open("results/filter/output_next.json", "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)
    print("✓ Empty JSON file created at results/filter/output_next.json")
    sys.exit()

print(f"Processing {len(test_texts)} texts...")

# Load model and tokenizer
model = load_model("med_classifier.h5")
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Convert text to sequences
sequences = tokenizer.texts_to_sequences(test_texts)
X = pad_sequences(sequences, maxlen=model.input_shape[1], padding="post")

# Predict
pred_probs = model.predict(X)

# Filter results based on probability threshold
filtered_text = []

for text, prob in zip(test_texts, pred_probs):
    probability = float(prob[0])  # Extract probability value
    
    if probability > 0.9:  # High confidence medicine names
        filtered_text.append({
            "text": text,
            "probability": probability
        })
        print(f"✓ MEDICINE: '{text}' (prob: {probability:.3f})")
    else:
        print(f"✗ OTHER: '{text}' (prob: {probability:.3f})")

# ALWAYS write to JSON file, whether empty or with results
if not filtered_text:
    print("No text passed the filter (probability > 0.9). Creating empty output file...")
    with open("results/filter/output_next.json", "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)
    print("✓ Empty JSON file created at results/filter/output_next.json")
else:
    print(f"\n{len(filtered_text)} text(s) passed the filter. Saving to JSON...")
    with open("results/filter/output_next.json", "w", encoding="utf-8") as f:
        json.dump(filtered_text, f, ensure_ascii=False, indent=4)
    print("✓ Results saved to results/filter/output_next.json")