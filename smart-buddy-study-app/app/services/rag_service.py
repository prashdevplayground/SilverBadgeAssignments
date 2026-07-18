# This service contains the retrieval-augmented generation pipeline.
# It is responsible for ingesting text into a vector database, retrieving relevant passages,
# and constructing grounded answers using a language model.

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline

from app.core.config import settings


class RAGService:
    # We keep the vector store and embeddings inside a single service object so the API can reuse them.
    def __init__(self) -> None:
        # We create the data directories only when the service is first used to keep startup lightweight.
        self.embeddings = None
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=120)
        self.llm = None
        self.llm_error: str | None = None
        self._initialized = False

    def _initialize(self) -> None:
        # This helper performs the heavier setup work lazily so the app can start quickly and tests remain reliable.
        if self._initialized:
            return

        settings.data_dir.mkdir(parents=True, exist_ok=True)
        settings.vector_db_dir.mkdir(parents=True, exist_ok=True)

        # We initialize sentence embeddings using a lightweight model that works well for semantic search.
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # We create a local Chroma vector database so documents can be stored and queried without a remote service.
        self.vector_store = Chroma(
            persist_directory=str(settings.vector_db_dir),
            embedding_function=self.embeddings,
            collection_name="smart_buddy_study",
        )

        # We initialize a small Hugging Face text generation pipeline for answer synthesis.
        # If the model cannot be downloaded or the environment is constrained, we keep the service functional by
        # falling back to a simple deterministic response later in the flow.
        try:
            self.llm = HuggingFacePipeline.from_model_id(
                model_id="google/flan-t5-small",
                task="text2text-generation",
                pipeline_kwargs={"max_new_tokens": 200},
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self.llm_error = str(exc)
            self.llm = None

        self._initialized = True

    def ingest_text(self, text: str, source: str | None = None) -> int:
        # This method turns raw content into document chunks and stores them in the vector database.
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        self._initialize()
        doc = Document(page_content=text.strip(), metadata={"source": source or "user-upload"})
        chunks = self.text_splitter.split_documents([doc])
        self.vector_store.add_documents(chunks)
        return len(chunks)

    def retrieve(self, question: str, top_k: int = 4) -> list[Document]:
        # We use semantic similarity to fetch the most relevant study passages for the user's question.
        self._initialize()
        return self.vector_store.similarity_search(question, k=top_k)

    def answer_question(self, question: str, top_k: int = 4) -> dict[str, Any]:
        # This method retrieves context and then builds a grounded answer using the retrieved passages.
        docs = self.retrieve(question, top_k=top_k)

        if not docs:
            return {
                "answer": "No study material has been indexed yet. Please ingest some content first.",
                "sources": [],
                "retrieved_documents": 0,
            }

        context = "\n\n".join([doc.page_content for doc in docs])
        prompt = (
            "Use the following study context to answer the question. "
            "If the answer is not contained in the context, say so clearly.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}"
        )

        if self.llm is None:
            result = (
                "I could not synthesize a full answer because the local language model is unavailable. "
                "The retrieved context suggests the answer is likely related to the indexed study material."
            )
        else:
            result = self.llm(prompt)[0]["generated_text"]

        sources = [
            {"source": doc.metadata.get("source", "unknown"), "snippet": doc.page_content[:220]}
            for doc in docs
        ]

        return {
            "answer": result.strip(),
            "sources": sources,
            "retrieved_documents": len(docs),
        }

    def build_study_plan(self, topic: str) -> list[str]:
        # We create a lightweight study plan based on the retrieved context for a given topic.
        docs = self.retrieve(topic, top_k=3)
        if not docs:
            return [
                "Ingest study notes for this topic so a plan can be generated.",
            ]

        context = "\n\n".join([doc.page_content for doc in docs])
        prompt = (
            "Create a short study plan with 4 bullet points for the topic. "
            f"Use the following context:\n{context}\n\nTopic: {topic}"
        )
        if self.llm is None:
            result = "- Review the core concepts\n- Practice with examples\n- Summarize the topic in your own words"
        else:
            result = self.llm(prompt)[0]["generated_text"]
        return [line.strip("- ") for line in result.splitlines() if line.strip()]


rag_service = RAGService()
