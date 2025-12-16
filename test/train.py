import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

samples = [
    # ✅ Medicine names
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


    # ❌ Non-medicine (other text on labels)
    ("Dosage: Take one tablet daily", "OTHER"),
    ("Dosage: 2 capsules every 6 hours", "OTHER"),
    ("KEEP OUT OF REACH OF CHILDREN", "OTHER"),
    ("Store below 25C", "OTHER"),
    ("Store in a cool dry place", "OTHER"),
    ("For questions call doctor", "OTHER"),
    ("Warnings: Alcohol interaction", "OTHER"),
    ("Batch no: 12345", "OTHER"),
    ("Expiry date: 2026", "OTHER"),
    ("Manufactured by: XYZ Pharma", "OTHER"),
    ("For oral use only", "OTHER"),
    ("Do not exceed recommended dose", "OTHER"),
    ("Caution: May cause drowsiness", "OTHER"),
    ("For external use only", "OTHER"),
    ("Take with meals", "OTHER"),
    ("Not recommended for children under 12", "OTHER"),
    ("Table", "OTHER"),
    ("Water", "OTHER"),
    ("Doctor", "OTHER"),
    ("Health", "OTHER"),
    ("Vitamin", "OTHER"),
    ("Strong", "OTHER"),
    ("Happy", "OTHER"),
    ("Pain", "OTHER"),
    ("Children", "OTHER"),
    ("Use", "OTHER"),
    ("Prescription", "OTHER")
]


texts, labels = zip(*samples)
labels = [1 if l == "MED_NAME" else 0 for l in labels]  # 1=MED, 0=OTHER

# 2. Tokenize text (convert words into numbers)
tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
X = pad_sequences(sequences, padding="post")
y = np.array(labels)

# 3. Build neural network
model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=8, input_length=X.shape[1]),
    GlobalAveragePooling1D(),
    Dense(16, activation="relu"),
    Dense(1, activation="sigmoid")  # output: probability MED_NAME vs OTHER
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])



model.fit(X, y, epochs=250, verbose=2)  # 🚀 Each epoch trains once on all data

model.save("med_classifier.h5")
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer,f)


