import json
import random
import os

# Define paths
train_path = "data/train_spacy.json"

# Check if file exists
if not os.path.exists(train_path):
    print("❌ No data found! Run spacious.py first.")
    exit()

# Load the data
with open(train_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"📊 Total Samples Generated: {len(data)}")
print("="*60)

# Pick 10 Random Samples
samples = random.sample(data, 10)

for i, entry in enumerate(samples, 1):
    text = entry[0]
    annotations = entry[1]['entities']
    
    print(f"Sample #{i}")
    print(f"📝 Text:    '{text}'")
    
    if len(annotations) == 0:
        print(f"🏷️  Labels:  [NONE] (This is a Negative Example)")
    else:
        print(f"🏷️  Labels:  {annotations}")
        # Show exactly what part of the text is labeled
        for start, end, label in annotations:
            span = text[start:end]
            print(f"   └── '{span}' = {label}")
            
    print("-" * 60)