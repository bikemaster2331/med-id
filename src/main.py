#!/usr/bin/env python3
"""
Main entry point for the Medicine Identification Application
This script orchestrates the entire pipeline: OCR -> Text Classification -> FDA API lookup
"""

import sys
import os

def run_pipeline():
    """Run the OCR pipeline to extract text from medicine images"""
    print("=== STEP 1: OCR TEXT EXTRACTION ===")
    try:
        from pipeline import process_pipe
        process_pipe()
        print("✓ OCR processing completed successfully\n")
    except Exception as e:
        print(f"✗ Error in OCR pipeline: {e}")
        sys.exit(1)

def run_prediction():
    """Run the ML prediction to filter medicine-related text"""
    print("=== STEP 2: MEDICINE TEXT CLASSIFICATION ===")
    try:
        import predict
        print("✓ Text classification completed successfully\n")
    except Exception as e:
        print(f"✗ Error in prediction step: {e}")
        sys.exit(1)

def run_api_client():
    """Run the FDA API client to get medicine information"""
    print("=== STEP 3: FDA API LOOKUP ===")
    try:
        import api_client
        print("✓ FDA API lookup completed successfully\n")
    except Exception as e:
        print(f"✗ Error in API client: {e}")
        sys.exit(1)

def main():
    """Main function that orchestrates the entire medicine identification process"""
    print("🔬 MEDICINE IDENTIFICATION SYSTEM")
    print("=" * 50)
    
    # Step 1: Extract text from medicine image using OCR
    run_pipeline()
    
    # Step 2: Classify and filter medicine-related text using ML model
    run_prediction()
    
    # Step 3: Look up medicine information using FDA API
    run_api_client()
    
    print("=" * 50)
    print("🎉 Medicine identification process completed!")

if __name__ == "__main__":
    main()