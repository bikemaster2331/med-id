import sys
import os

def run_pipeline():
    print("=== STEP 1: OCR TEXT EXTRACTION ===")
    try:
        from obj_detection import process_pipe
        process_pipe()
        print("✓ OCR processing completed successfully\n")
    except Exception as e:
        print(f"✗ Error in OCR pipeline: {e}")
        sys.exit(1)

def run_prediction():
    print("=== STEP 2: MEDICINE TEXT CLASSIFICATION ===")
    try:
        import predict
        print("✓ Text classification completed successfully\n")
    except Exception as e:
        print(f"✗ Error in prediction step: {e}")
        sys.exit(1)

def run_api_client():
    print("=== STEP 3: FDA API LOOKUP ===")
    try:
        import api_client
        
        print("✓ FDA API lookup completed successfully\n")
    except Exception as e:
        print(f"✗ Error in API client: {e}")
        sys.exit(1)

def main():

    print("🔬 MEDICINE IDENTIFICATION SYSTEM")
    print("=" * 50)
    run_pipeline() 
    run_prediction()    
    run_api_client()
    
    print("=" * 50)
    print("🎉 Medicine identification process completed!")

if __name__ == "__main__":
    main()