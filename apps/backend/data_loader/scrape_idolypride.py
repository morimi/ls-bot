import requests
from bs4 import BeautifulSoup, NavigableString
import json
from urllib.parse import urljoin

BASE_URL = "https://idolypride.jp"
CHARACTER_PATHS = [
    "/character/kana",
    "/character/ai-komiyama",
    "/character/aoi-igawa",
    "/character/chisa-shiraishi",
    "/character/haruko-saeki",
]

OUTPUT_PATH = "data/character_data.json"


def extract_contexts_from_article(article):
    contexts = []
    for tag in article.find_all(True, recursive=True):
        if tag.name == "nav":
            continue
        # aria-label, alt, title属性
        texts = []
        for attr in ["aria-label", "alt", "title"]:
            if tag.has_attr(attr):
                texts.append(tag[attr])
        # 1タグ内の全テキストノードを連結（改行タグや空白は無視）
        tag_text = "".join([s for s in tag.strings if isinstance(s, NavigableString) and s.strip()])
        if tag_text:
            texts.append(tag_text.strip())
        # 1つの文脈としてまとめる
        if texts:
            context = " ".join(texts)
            # 属性名＋値のペアを検出して連結（例: <span>身長</span><span>166cm</span>）
            next_sibling = tag.find_next_sibling()
            if next_sibling and next_sibling.name == tag.name:
                sibling_text = "".join([s for s in next_sibling.strings if isinstance(s, NavigableString) and s.strip()])
                if sibling_text and len(sibling_text) < 30 and len(tag_text) < 30:
                    context = f"{tag_text.strip()} {sibling_text.strip()}"
            contexts.append(context)
    return contexts

def main():
    all_data = []
    for path in CHARACTER_PATHS:
        url = urljoin(BASE_URL, path)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "html.parser")
        for article in soup.find_all("article"):
            contexts = extract_contexts_from_article(article)
            for ctx in contexts:
                all_data.append({
                    "text": ctx,
                    "url": url,
                    "source_file": path
                })
    # 保存
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main() 