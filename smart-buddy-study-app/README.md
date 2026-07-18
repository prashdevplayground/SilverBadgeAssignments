# Smart Buddy Study

This project is a fresh, modern implementation of a study assistant built with FastAPI, LangChain, and a local vector database. The app supports end-to-end RAG workflows, including ingestion, semantic retrieval, answer generation, and study-plan creation.

## What is included

- FastAPI backend with documented endpoints
- Local Chroma vector database for embedding search
- LangChain integration for chunking and retrieval
- Hugging Face sentence embeddings and lightweight LLM generation
- Docker and Docker Compose support for containerized deployment

## Quick start

1. Create and activate a Python environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run the service locally with `uvicorn app.main:app --reload`.
4. Open the API docs at `http://127.0.0.1:8000/docs`.

## Docker

Run the app with:

```bash
docker compose up --build
```

## Example API usage

### Ingest study notes

```bash
curl -X POST http://127.0.0.1:8000/api/ingest \
  -H 'Content-Type: application/json' \
  -d '{"text": "Python lists are mutable sequences used to store ordered items.", "source": "python-notes"}'
```

### Ask a question

```bash
curl -X POST http://127.0.0.1:8000/api/ask \
  -H 'Content-Type: application/json' \
  -d '{"question": "What are Python lists?", "top_k": 3}'
```

### Get a study plan

```bash
curl http://127.0.0.1:8000/api/study-plan/python
```
