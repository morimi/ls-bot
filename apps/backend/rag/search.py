from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import chromadb
from chromadb.config import Settings
from openai import OpenAI
from dotenv import load_dotenv
import json
import re

router = APIRouter()

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

RAG_DOCS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../rag_docs.json'))

# キャラクター名リスト
CHARACTER_NAMES = [
    "kana", "KANA", "カナ", "こみやま愛", "ai-komiyama", "AI KOMIYAMA", "小宮山愛",
    "aoi-igawa", "AOI IGAWA", "井川葵", "ちさ白石", "chisa-shiraishi", "CHISA SHIRAISHI", "白石千紗",
    "さえきはるこ", "haruko-saeki", "HARUKO SAEKI", "佐伯遙子"
]

# キャラクター名のエイリアス（表記ゆれ対応）
CHARACTER_ALIASES = {
    "小宮山愛": "小美山愛",
    "こみやま": "小美山愛",
    "あい": "小美山愛",
    "ai-komiyama": "小美山愛",
    "AI KOMIYAMA": "小美山愛",
    "AIKOMIYAMA": "小美山愛",
    "komiyama ai": "小美山愛",
    # 他キャラも必要に応じて追加
}

def normalize_character_name(name):
    return CHARACTER_ALIASES.get(name, name)

# 質問文からキャラクター名を抽出
def extract_character_name(query):
    for name in CHARACTER_NAMES:
        if name.lower() in query.lower():
            return normalize_character_name(name)
    # ひらがな・カタカナ・漢字の「〇〇について教えて」パターンも抽出
    m = re.search(r"([\wぁ-んァ-ン一-龥]+)[についてをはが、\s]*教えて", query)
    if m:
        return normalize_character_name(m.group(1))
    return None

class SearchRequest(BaseModel):
    query: str
    n_results: int = 5

@router.post("")
async def search_endpoint(body: SearchRequest):
    query = body.query.strip()
    n_results = body.n_results
    if not query:
        raise HTTPException(status_code=400, detail="query required")

    # まずrag_docs.jsonで完全一致・部分一致を探す
    with open(RAG_DOCS_PATH, encoding="utf-8") as f:
        rag_docs = json.load(f)
    # キャラクター名抽出
    char_name = extract_character_name(query)
    keyword_hits = []
    correct_name_message = None
    if char_name:
        # 入力名がエイリアスだった場合、正しい表記を案内
        for alias, correct in CHARACTER_ALIASES.items():
            if char_name == correct and alias in query:
                correct_name_message = f"ご質問のキャラクターの正しい表記は「{correct}」です。以下、プロフィール情報です。"
                break
        # 完全一致
        exact_matches = [doc for doc in rag_docs if doc["text"].lower() == char_name.lower()]
        # 部分一致
        alias = CHARACTER_ALIASES.get(char_name, None)
        partial_matches = [doc for doc in rag_docs if (char_name.lower() in doc["text"].lower() or (alias and alias in doc["text"])) and doc not in exact_matches]
        keyword_hits = exact_matches + partial_matches
    # 通常のクエリでも完全一致・部分一致
    exact_matches = [doc for doc in rag_docs if doc["text"].lower() == query.lower()]
    partial_matches = []
    if len(query) > 2:
        partial_matches = [doc for doc in rag_docs if query.lower() in doc["text"].lower() and doc not in exact_matches]
    keyword_hits += [doc for doc in exact_matches + partial_matches if doc not in keyword_hits]

    # ベクトル検索
    res = client.embeddings.create(input=[query], model="text-embedding-3-small")
    qvec = res.data[0].embedding
    chroma_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data_loader/chromadb_store"))
    chroma_client = chromadb.PersistentClient(path=chroma_dir)
    collection = chroma_client.get_or_create_collection("idolypride_docs")
    results = collection.query(query_embeddings=[qvec], n_results=n_results)
    hits = []
    for i in range(len(results['ids'][0])):
        hits.append({
            'id': results['ids'][0][i],
            'text': results['documents'][0][i],
            'score': results['distances'][0][i],
            **results['metadatas'][0][i],
        })

    # keyword_hitsを優先して返す（重複除去）
    seen = set()
    merged = []
    if correct_name_message:
        merged.append({'text': correct_name_message, 'url': '', 'score': 0})
    for doc in keyword_hits:
        key = (doc['text'], doc['url'])
        if key not in seen:
            merged.append(doc)
            seen.add(key)
    for hit in hits:
        key = (hit['text'], hit.get('url', ''))
        if key not in seen:
            merged.append(hit)
            seen.add(key)
    return {'results': merged[:n_results]} 