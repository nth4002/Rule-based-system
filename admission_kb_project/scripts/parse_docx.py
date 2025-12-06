import os
from docx import Document
import json

INPUT_DIR = "../data/raw_docs"
OUTPUT_FILE = "../data/extracted/raw_text.json"

def extract_text_from_docx(path):
    doc = Document(path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)

def main():
    all_docs = {}

    for fname in os.listdir(INPUT_DIR):
        if fname.endswith(".docx"):
            path = os.path.join(INPUT_DIR, fname)
            print(f"Parsing {fname}...")
            text = extract_text_from_docx(path)
            all_docs[fname] = text

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_docs, f, ensure_ascii=False, indent=2)

    print("Done. Output saved to:", OUTPUT_FILE)

if __name__ == "__main__":
    main()
