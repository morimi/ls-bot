import json
import os
from openai import OpenAI
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings

INPUT_PATH = "rag_docs.json"
CHROMA_DIR = "chromadb_store"
COLLECTION_NAME = "idolypride_docs"

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

def main():
    with open(INPUT_PATH, encoding="utf-8") as f:
        docs = json.load(f)
    texts = [doc["text"] for doc in docs]
    metadatas = [{"url": doc["url"], "source_file": doc["source_file"]} for doc in docs]
    # ベクトル化
    embeddings = []
    for i in range(0, len(texts), 100):
        chunk = texts[i:i+100]
        res = client.embeddings.create(input=chunk, model="text-embedding-3-small")
        embeddings.extend([e.embedding for e in res.data])
    # ChromaDB保存
    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    if COLLECTION_NAME in [c.name for c in chroma_client.list_collections()]:
        chroma_client.delete_collection(COLLECTION_NAME)
    collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
    ids = [f"doc_{i}" for i in range(len(texts))]
    collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)
    print(f"{len(texts)} docs saved to ChromaDB.")

if __name__ == "__main__":
    main() 