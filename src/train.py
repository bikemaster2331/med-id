samples = [
    ("Paracetamol", "MED_NAME"),
    ("Ibuprofen", "MED_NAME"),
    ("Amoxicillin", "MED_NAME"),
    ("KEEP OUT OF REACH OF CHILDREN", "OTHER"),
    ("Dosage: Take one tablet daily", "400mg", "OTHER"),
    ("Warnings: Do not use with alcohol", "OTHER")
]


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

texts, labels = zip(*samples)

model = Pipeline([
    ("vectorizer", CountVectorizer(ngram_range=(1,2))),
    ("classifier", LogisticRegression())
])

model.fit(texts,labels)

test_texts = ["Cetirizine", "Store below 400c"]
prediction = model.predict(test_texts)
print(list(zip(test_texts, prediction)))