samples = [
    ("Paracetamol", "MED_NAME"),
    ("Ibuprofen", "MED_NAME"),
    ("Amoxicillin", "MED_NAME"),
    ("Metformin", "MED_NAME"),
    ("Dosage: Take one tablet daily", "OTHER"),
    ("KEEP OUT OF REACH OF CHILDREN", "OTHER"),
    ("Store below 25C", "OTHER"),
    ("For questions call doctor", "OTHER"),
    ("Warnings: Alcohol interaction", "OTHER"),
    ("Batch no: 12345", "OTHER"),
    ("Expiry date: 2026", "OTHER")
]



from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

texts, labels = zip(*samples)

model = Pipeline([
    ("vectorizer", CountVectorizer(analyzer="char", ngram_range=(3,5))),
    ("classifier", LogisticRegression())
])

model.fit(texts,labels)

test_texts = ["Cetirizine", "Store below 400c"]
prediction = model.predict(test_texts)
print(list(zip(test_texts, prediction)))