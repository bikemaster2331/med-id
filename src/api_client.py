import requests
import os
import json
import sys
# Import the correct client (new SDK) and error handling
from google import genai 
from google.genai.errors import APIError

# Global variables to hold the client and its status
gemini_client = None
HAS_GEMINI = False

def setup_gemini():
    """Initializes the Gemini API client."""
    global gemini_client, HAS_GEMINI

    try:
        # NOTE: Using "GEMINI_API_KEY" is standard, but the user's setup might be using "GEMINI_KEY"
        # We respect the key name used in the function definition for now.
        api_key = os.getenv("GEMINI_KEY")
        if not api_key:
            print("⚠️ GEMINI_KEY not found in environment. LLM summarization disabled.")
            HAS_GEMINI = False
            return
            
        # Initialize the client using the key
        gemini_client = genai.Client(api_key=api_key)
        HAS_GEMINI = True
        print("✅ Gemini Initialized...")
        
    except Exception as e:
        print(f"❌ Gemini setup failed: {e}")
        HAS_GEMINI = False


def generate_summary(drug_name, purpose, indications, dosage):
    """
    Sends structured drug information to the Gemini model for summarization.
    """
    global gemini_client, HAS_GEMINI

    if not HAS_GEMINI:
        return "LLM summarization skipped: Gemini API client not available."
    
    # 1. Format the data into a single, comprehensive string for the LLM
    drug_info_text = f"""
    DRUG NAME: {drug_name}

    PURPOSE:
    {purpose}

    INDICATIONS AND USAGE:
    {indications}

    DOSAGE:
    {dosage}
    """

    # 2. Define the System Instruction (The instruction for the LLM)
    system_instruction = """
You rewrite FDA drug label data into a strict, concise 3-bullet summary.

Rules:
1. Do NOT add explanations, context, or details not present in the raw text.
2. Do NOT exceed 1 short sentence per bullet.
3. Do NOT restate chemical classes, history, or mechanism unless explicitly in the raw text.
4. Do NOT expand acronyms.
5. Preserve meaning strictly; do not speculate.
6. Output format must be EXACTLY:

• Purpose: <1 short sentence from raw PURPOSE>
• Indications: <1 short sentence from raw INDICATIONS AND USAGE>
• Dosage: <1 short sentence from raw DOSAGE AND ADMINISTRATION>

No intro text. No conclusion. No markdown. No bold formatting.
"""

    print("\n\n🧠 Sending data to Gemini for summarization...")
    
    try:
        # 3. Call the Gemini API using gemini-2.5-flash
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash', # Use the fast model for summarization
            contents=[drug_info_text],
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2 # Keep the output factual
            )
        )

        # 4. Extract and return the summary text
        return response.text

    except APIError as e:
        print(f"✗ Error during Gemini API call: {e}")
        return "Failed"
    except Exception as e:
        print(f"✗ An unexpected error occurred during summarization: {e}")
        return "Failed"

# =========================================================================
# === START SCRIPT EXECUTION ===
# =========================================================================

# Load the filtered text
with open("results/filter/output_next.json", "r", encoding="utf-8") as f:
    filtered_text = json.load(f)

# Initialize Gemini before any data processing
setup_gemini() 

# Extract the drug name from the list
data = [item["text"] for item in filtered_text]
if len(data) == 0:
    print("No data passed, please try again")
    sys.exit()

# Extract the drug name for searching
drug_name = data[0]

print(f"Searching for drug: {drug_name}")
api_key = os.getenv("OPEN_FDA_KEY")


url = "https://api.fda.gov/drug/label.json"

# Construct a targeted search query
search_query = f'{drug_name}'

params = {
    "search": search_query, 
    "limit": 1,
    "api_key": api_key
}


print("\n--- FDA API DEBUG INFO ---")
print(f"Base URL: {url}")
print(f"Search Query Parameter (search): {search_query}")


response = requests.get(url, params=params)
fda_data = response.json()

if "results" in fda_data:
    result = fda_data["results"][0]

    # 1. Extract the raw data
    found_brand = result.get("openfda", {}).get("brand_name", ["N/A"])[0]
    
    raw_purpose = result.get("purpose", ["N/A"])[0]
    raw_indications = result.get("indications_and_usage", ["N/A"])[0]
    raw_dosage = result.get("dosage_and_administration", ["N/A"])[0]

    # 2. Call the LLM Summarization Function
    summary_text = generate_summary(
        drug_name=found_brand,
        purpose=raw_purpose,
        indications=raw_indications,
        dosage=raw_dosage
    )

    # 3. Display the Summarized Output
    print("\n\n======================================================= =")
    print("🧠 GEMINI SUMMARIZATION FOR GENERAL AUDIENCE")
    print("========================================================")
    print(summary_text)
    print("========================================================")

else:
    print(f"No results found for {drug_name} using targeted search.")

print("\nThank you for using MED_ID!")