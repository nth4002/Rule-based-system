import json
import re

INPUT_FILE = "../data/extracted/raw_text.json"
OUTPUT_FILE = "../kb/facts.json"

def extract_major(line):
    """Example: 'Ngành Công nghệ thông tin (7480201)'"""
    match = re.search(r"Ngành\s+(.+?)\s*\((\d{7})\)", line)
    if match:
        name, code = match.groups()
        return ("major", code, name)
    return None

def extract_admission_method(line):
    """Example: 'Phương thức xét tuyển 1: Xét điểm THPT'"""
    if "Phương thức" in line:
        return ("method", line.strip())
    return None

def extract_score(line):
    """Example: 'Điểm chuẩn 2023: 24.5'"""
    match = re.search(r"Điểm chuẩn.*?(\d{2}\.?\d?)", line)
    if match:
        score = float(match.group(1))
        return ("score", score)
    return None

def extract_entities(text):
    facts = []
    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        f1 = extract_major(line)
        if f1: facts.append(f1)

        f2 = extract_admission_method(line)
        if f2: facts.append(f2)

        f3 = extract_score(line)
        if f3: facts.append(f3)

    return facts

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        docs = json.load(f)

    all_facts = []

    for filename, content in docs.items():
        print(f"Extracting from {filename}...")
        facts = extract_entities(content)
        all_facts.extend(facts)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_facts, f, ensure_ascii=False, indent=2)

    print("Done. Facts saved to:", OUTPUT_FILE)

if __name__ == "__main__":
    main()
