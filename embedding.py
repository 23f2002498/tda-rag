import os
import glob
import uuid
import json
import requests
import chromadb

# CONFIG
OLLAMA_URL = "http://192.168.1.11:11434/api/embeddings"  # replace with your remote Ollama URL
MODEL_NAME = "dengcao/Qwen3-Embedding-0.6B:Q8_0"
DATA_DIR = "data/md"  # directory with cleaned Markdown files

# Load Markdown files
def load_markdown_files(directory):
    md_data = []
    for filepath in glob.glob(os.path.join(directory, "*.md")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                md_data.append({
                    "id": str(uuid.uuid4()),
                    "content": content,
                    "filename": os.path.basename(filepath)
                })
    return md_data

# Use remote Ollama API to get embeddings
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

# Index in ChromaDB
def embed_and_store(directory):
    docs = load_markdown_files(directory)

    client = chromadb.PersistentClient(path="chroma_store")
    collection = client.get_or_create_collection(name="md_docs")

    for doc in docs:
        emb = get_embedding(doc["content"])
        if emb:
            collection.add(
                ids=[doc["id"]],
                documents=[doc["content"]],
                embeddings=[emb],
                metadatas=[{"source": doc["filename"]}]
            )
            print(f"[+] Embedded and stored: {doc['filename']}")
        else:
            print(f"[WARN] Skipped: {doc['filename']}")

embed_and_store(DATA_DIR)
