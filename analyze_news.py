import os
import glob
import json
import datetime
import time
import google.generativeai as genai

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "raw_papers")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
DIGESTS_DIR = os.path.join(PUBLIC_DIR, "digests")
MANIFEST_FILE = os.path.join(DIGESTS_DIR, "manifest.json")

# System Instructions for the AI
SYSTEM_INSTRUCTION = """You are an expert AI Finance Agent. Perform a detailed analytical breakdown of the provided newspaper. Structure the output in Markdown with these exact sections:
## 1. Macroeconomic Context & Policy Updates
## 2. Equity Markets & Corporate Actions (Highlight stock movements and M&A)
## 3. Commodities & Global Trends (Focus specifically on Physical Gold, Silver, and energy)
## 4. Academic Application & Financial Concepts (Explain 2-3 complex financial events from the news using MBA-level theory like Valuation, Arbitrage, or Technical Analysis)."""

def main():
    # Initialize the client
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return
        
    genai.configure(api_key=api_key)

    # Find the first PDF in raw_papers
    pdf_files = glob.glob(os.path.join(RAW_DIR, "*.pdf"))
    if not pdf_files:
        print("No PDF files found in raw_papers/. Exiting.")
        return
    
    pdf_path = pdf_files[0]
    print(f"Processing: {pdf_path}")
    
    # Upload to Gemini File API
    print("Uploading file to Gemini...")
    uploaded_file = genai.upload_file(path=pdf_path)
    
    # Wait for the file to be processed
    print("Waiting for file processing...")
    while uploaded_file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(2)
        uploaded_file = genai.get_file(uploaded_file.name)
    
    print("\nFile ready.")
    
    try:
        # Generate content
        print("Generating digest...")
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=SYSTEM_INSTRUCTION
        )
        
        response = model.generate_content([uploaded_file, "Please analyze this daily newspaper."])
        
        # Save output
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        digest_filename = f"digest-{date_str}.md"
        digest_path = os.path.join(DIGESTS_DIR, digest_filename)
        
        os.makedirs(DIGESTS_DIR, exist_ok=True)
        
        with open(digest_path, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"Digest saved to: {digest_path}")
        
        # Update manifest
        update_manifest(digest_filename, date_str)
        
    finally:
        # Clean up
        print("Deleting file from Gemini...")
        genai.delete_file(uploaded_file.name)
        
        # Optional: Delete the local PDF to clear the folder for tomorrow
        os.remove(pdf_path)
        print("Deleted local PDF.")

def update_manifest(filename, date_str):
    os.makedirs(DIGESTS_DIR, exist_ok=True)
        
    manifest = []
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, "r") as f:
            try:
                manifest = json.load(f)
            except json.JSONDecodeError:
                pass
                
    # Add new entry at the beginning
    entry = {"date": date_str, "file": filename}
    if entry not in manifest:
        manifest.insert(0, entry)
        
    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    main()
