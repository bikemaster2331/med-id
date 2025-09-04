import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle


# Load trained model
model = load_model("med_classifier.h5")

# Load tokenizer
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Example text inputs
test_texts = ["ambroxixilin"]

# Convert text to sequences
sequences = tokenizer.texts_to_sequences(test_texts)
X = pad_sequences(sequences, maxlen=model.input_shape[1], padding="post")

# Predict
pred_probs = model.predict(X)
pred_labels = ["MED_NAME" if p > 0.5 else "OTHER" for p in pred_probs]

# Print results
for text, label, prob in zip(test_texts, pred_labels, pred_probs):
    print(f"Text: {text} -> Prediction: {label} (prob={prob[0]:.3f})")
