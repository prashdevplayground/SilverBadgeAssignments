# This module defines the request and response models used by the API.
# Using Pydantic models makes the API contract explicit and improves validation.

from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    # The client sends text that should become part of the study knowledge base.
    text: str = Field(..., min_length=1, description="Raw study notes or documents to ingest")
    source: str | None = Field(default=None, description="Optional label for the source of the content")


class AskRequest(BaseModel):
    # The user asks a question that should be answered using retrieved study context.
    question: str = Field(..., min_length=1, description="Question to answer from the study corpus")
    top_k: int = Field(default=4, ge=1, le=10, description="Number of retrieved passages to use")


class SourceReference(BaseModel):
    # Each source reference lets the client inspect where the answer came from.
    source: str
    snippet: str


class AskResponse(BaseModel):
    # This response includes the answer and the supporting evidence retrieved from the vector store.
    question: str
    answer: str
    sources: list[SourceReference]
    retrieved_documents: int


class StudyPlanResponse(BaseModel):
    # This response returns a simple structured study plan generated from retrieved knowledge.
    topic: str
    plan: list[str]
