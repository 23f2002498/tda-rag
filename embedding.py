import os
import glob
import uuid
import json
import requests
import re
import chromadb
# from sentence_transformers import SentenceTransformer
# embed_model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

# === CONFIG ===
OLLAMA_URL = "http://192.168.1.11:11434/api/embeddings"
MODEL_NAME = "dengcao/Qwen3-Embedding-0.6B:Q8_0"
DATA_DIR = "data/md"
CHROMA_DIR = "chroma_store"
COLLECTION_NAME = "md_docs"

# === Helper: Extract URL from Markdown ===
def extract_url(text):
    match = re.search(r"\*\*URL\*\*: \[([^\]]+)\]", text)
    return match.group(1) if match else None

# === Helper: Load .md files ===
def load_markdown_files(directory):
    md_data = []
    for filepath in glob.glob(os.path.join(directory, "*.md")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                md_data.append({
                    "id": str(uuid.uuid4()),
                    "content": content,
                    "filename": os.path.basename(filepath),
                    "url": extract_url(content)
                })
    return md_data

# === Helper: Get embeddings from remote Ollama ===
def get_embedding(text):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": text
        })
        response.raise_for_status()
        return response.json()["embedding"]
    except Exception as e:
        print(f"[ERROR] Embedding failed: {e}")
        return None

# === Main: Embed and store in ChromaDB ===
def embed_and_store(directory):
    docs = load_markdown_files(directory)

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    for doc in docs:
        emb = get_embedding(doc["content"])
        if not emb:
            print(f"[WARN] Skipping: {doc['filename']}")
            continue

        source = doc["url"] if doc["url"] else doc["filename"]

        collection.add(
            ids=[doc["id"]],
            documents=[doc["content"]],
            embeddings=[emb],
            metadatas=[{"source": source}]
        )
        print(f"[+] Stored: {doc['filename']} → {source}")

if __name__ == "__main__":
    embed_and_store(DATA_DIR)
