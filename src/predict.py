import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import json

with open("output.json", "r", encoding="utf-8") as f:
    extracted_text = json.load(f)

filtered_text = []

model = load_model("med_classifier.h5")

# Load tokenizer
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Example text inputs
test_texts = [item["text"] for item in extracted_text]

# Convert text to sequences
sequences = tokenizer.texts_to_sequences(test_texts)
X = pad_sequences(sequences, maxlen=model.input_shape[1], padding="post")

# Predict
pred_probs = model.predict(X)

for text, prob in zip(test_texts, pred_probs):
    if prob > 0.5: 
        filtered_text.append({
            "text": text,
            "probability": float(prob[0]) 
        })

print(filtered_text)

# pred_labels = ["MED_NAME" if p > 0.5 else "OTHER" for p in pred_probs]

# Print results
# for text, label, prob in zip(test_texts, pred_labels, pred_probs):
#     print(f"Text: {text} -> Prediction: {label} (prob={prob[0]:.3f})")