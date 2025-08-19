import json
import re
import os

INPUT_PATH = "data/character_data.json"
OUTPUT_PATH = "rag_docs.json"

def clean_text(text):
    # 連続スペース・改行を1つに
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def main():
    with open(INPUT_PATH, encoding="utf-8") as f:
        data = json.load(f)
    rag_docs = []
    for item in data:
        cleaned = clean_text(item["text"])
        if cleaned:
            rag_docs.append({
                "text": cleaned,
                "url": item["url"],
                "source_file": item["source_file"]
            })
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(rag_docs, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main() 