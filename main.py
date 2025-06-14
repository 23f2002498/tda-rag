from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import base64
import os
import io
import pytesseract
from PIL import Image
from sentence_transformers import SentenceTransformer, util
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Load embedding model locally
embed_model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

# ChromaDB setup
chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="chroma_store"))
collection = chroma_client.get_or_create_collection(
    name="md-docs",
    embedding_function=SentenceTransformerEmbeddingFunction(embed_model)
)

class QuestionPayload(BaseModel):
    question: str
    image: str  # base64 string

def get_embedding(text: str):
    """Generate embedding vector for the input text."""
    return embed_model.encode([text])[0]

import requests

def llm_ans(question: str, context_snippets: list) -> str:
    # Variables
    model = "gpt-4o-mini"
    api_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"

    # Construct system + user prompt using RAG-style grounding
    system_prompt = "You are a helpful assistant. Use the provided context to answer the question as accurately as possible."
    context = "\n\n".join(context_snippets)
    user_prompt = f"Context:\n{context}\n\nQuestion:\n{question}"

    headers = {
        "Content-Type": "application/json"
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(api_url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return "Failed to retrieve answer from LLM."


@app.post("/api/")
def process_question(payload: QuestionPayload):
    question = payload.question
    image_data = base64.b64decode(payload.image)
    
    # OCR extraction
    try:
        img = Image.open(io.BytesIO(image_data))
        ocr_text = pytesseract.image_to_string(img)
        question_full = f"{question}\n{ocr_text.strip()}"
    except Exception as e:
        question_full = question  # fallback if OCR fails

    # Embed the query
    question_embedding = get_embedding(question_full)

    # Query ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    # Prepare context and links
    context_snippets = results['documents'][0]
    links = []
    for doc, meta in zip(context_snippets, results['metadatas'][0]):
        links.append({
            "url": meta.get("source", ""),
            "text": doc[:200]  # snippet
        })

    # Call LLM with retrieved context
    answer = llm_ans(question_full, context_snippets)

    return JSONResponse(content={
        "answer": answer,
        "links": links
    })

