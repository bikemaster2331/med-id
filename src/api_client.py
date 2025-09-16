import requests
import os
import json

with open("results/filter/output_next.json", "r", encoding="utf-8") as f:
    filtered_text = json.load(f)


data = [item["text"] for item in filtered_text]

api_key = os.getenv("OPEN_FDA_KEY")

url = "https://api.fda.gov/drug/label.json"
params = {
    "search": data,   # example drug
    "limit": 1,
    "api_key": api_key
}

response = requests.get(url, params=params)
data = response.json()

if "results" in data:
    result = data["results"][0]
    

    print("Purpose:", result.get("purpose", ["N/A"])[0])
    print("="*100)
    print("Indications and usage:", result.get("indications_and_usage", ["N/A"])[0])
    print("="*100)
    print("Dosage:", result.get("dosage_and_administration", ["N/A"])[0])
else:
    print("No results found")