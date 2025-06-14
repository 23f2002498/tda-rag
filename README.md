# TDS MAY 2025 Project 1
FastAPI OCR + Embedding Q&A API Built with data sourced from IITM discourse and course pages

This project is a lightweight FastAPI-based API that allows users to ask questions, optionally attach an image, and receive contextual answers using OCR and embedding-based retrieval.

## 🚀 Features

- Accepts a question via POST request
- Optionally processes an image (base64) to extract text using Tesseract OCR
- Embeds the question + image text using a transformer model
- Retrieves relevant Markdown document snippets from a ChromaDB vector store
- Sends retrieved context and question to an LLM to generate a precise answer
- Returns answer along with document links/snippets

## 🔧 Technologies Used

- **FastAPI** for API handling
- **Tesseract OCR** for text extraction from images
- **Hugging Face Inference API** for generating sentence embeddings
- **ChromaDB** as a lightweight vector database
- **OpenAI-compatible proxy** for generating answers

## 🔐 Notes

- Ensure `Tesseract OCR` is installed in your deployment environment
- Environment variables like API keys should be kept secret (e.g., `.env`)
- Designed for self-hosted or private deployments

## 📦 API Endpoint

**POST** `/api/`

### Request Body

```json
{
  "question": "What is this project about?",
  "image": "base64_encoded_image_string (optional)"
}
````

### Response

```json
{
  "answer": "This is a Q&A API powered by embeddings and OCR.",
  "links": [
    {
      "url": "https://example.com/doc1",
      "text": "First 200 characters of the related document..."
    }
  ]
}
```

## 🧪 Example Usage

You can test the API using [Postman](https://postman.com), `curl`, or a frontend.

For deployment, be sure to configure environment variables and include system dependencies like `tesseract-ocr`.

