from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import io
import base64
import pytesseract
from PIL import Image
import chromadb
import requests
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Initialize FastAPI
app = FastAPI()

load_dotenv()
api_key = os.getenv("API_KEY")
hf_token = os.getenv("HF_TOKEN")  # Hugging Face token

client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["HF_TOKEN"],
)

# ChromaDB setup (collection renamed)
chroma_client = chromadb.PersistentClient(path="chroma_store")
collection = chroma_client.get_or_create_collection(name="md_docs")

# Pydantic model
class QuestionPayload(BaseModel):
    question: str
    image: Optional[str] = None  # base64-encoded image string

# Generate embedding via Hugging Face Inference API
def get_embedding(text: str):
    try:
        result = client.feature_extraction(
            text=text,
            model="sentence-transformers/all-MiniLM-L6-v2",
        )
        return result  # This is your embedding vector
    except Exception as e:
        print(f"[EMBEDDING ERROR] {e}")
        return None

# Call remote LLM with context
def llm_ans(query: str, context: List[str]) -> str:
    api_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    model = "gpt-4o-mini"
    headers = {"Content-Type": "application/json"}
    headers["Authorization"] = f"Bearer {api_key}"

    messages = [
        {"role": "system", "content": "Answer the user query using the following context. If no context is relevantand you have no knowledge on it dont't hallucinate rather say you don’t know.Always reply with exact details and not speculation especially when it is regarding dates"},
        {"role": "user", "content": f"Question: {query}\n\nContext:\n{chr(10).join(context)}"}
    ]

    try:
        response = requests.post(api_url, json={
            "model": model,
            "stream": False,
            "messages": messages
        }, headers=headers, timeout=20)

        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response from LLM.")
    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return f"LLM error: {e}"

# POST endpoint
@app.post("/api/")
def process_question(payload: QuestionPayload):
    question = payload.question.strip()
    image_data = payload.image
    ocr_text = ""

    # OCR if image provided
    if image_data:
        try:
            image_bytes = base64.b64decode(image_data)
            img = Image.open(io.BytesIO(image_bytes))
            ocr_text = pytesseract.image_to_string(img).strip()
        except Exception as e:
            print(f"[OCR ERROR] {e}")

    # Combine question and OCR text
    full_input = f"{question}\n{ocr_text}".strip()

    # Embed question
    embedding = get_embedding(full_input)
    if embedding is None:
        return JSONResponse(status_code=500, content={"error": "Embedding generation failed."})

    # Query ChromaDB
    try:
        results = collection.query(query_embeddings=[embedding], n_results=3)
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
    except Exception as e:
        print(f"[ChromaDB ERROR] {e}")
        return JSONResponse(status_code=500, content={"error": "ChromaDB query failed."})

    # Prepare context + links
    context_snippets = documents
    links = [{
        "url": meta.get("source", ""),
        "text": doc[:200]
    } for doc, meta in zip(documents, metadatas)]

    # Get LLM answer
    answer = llm_ans(full_input, context_snippets)

    return JSONResponse(content={
        "answer": answer,
        "links": links
    })
