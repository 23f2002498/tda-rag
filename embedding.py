import os
import glob
import uuid
import re
import chromadb
from sentence_transformers import SentenceTransformer

# === CONFIG ===
DATA_DIR = "data/md"
CHROMA_DIR = "chroma_store"
COLLECTION_NAME = "md_docs"

# === Load embedding model ===
embed_model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dimensional

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

# === Helper: Get embedding from local model ===
def get_embedding(text):
    try:
        return embed_model.encode(text).tolist()
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
