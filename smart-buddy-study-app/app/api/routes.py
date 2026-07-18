# This file defines the API routes for ingesting material, answering questions, and generating plans.
# The routes expose the RAG capabilities implemented by the service layer as a clean HTTP API.

from fastapi import APIRouter, HTTPException

from app.models.schemas import AskRequest, AskResponse, IngestRequest, SourceReference, StudyPlanResponse
from app.services.rag_service import rag_service

router = APIRouter()


@router.post("/ingest", response_model=dict[str, int])
async def ingest_material(payload: IngestRequest) -> dict[str, int]:
    # The ingestion endpoint accepts user-supplied study content and stores it in the vector database.
    try:
        chunks = rag_service.ingest_text(payload.text, source=payload.source)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"stored_chunks": chunks}


@router.post("/ask", response_model=AskResponse)
async def ask_question(payload: AskRequest) -> AskResponse:
    # The ask endpoint retrieves relevant passages and synthesizes an answer for the client.
    result = rag_service.answer_question(payload.question, top_k=payload.top_k)
    return AskResponse(
        question=payload.question,
        answer=result["answer"],
        sources=[SourceReference(**source) for source in result["sources"]],
        retrieved_documents=result["retrieved_documents"],
    )


@router.get("/study-plan/{topic}", response_model=StudyPlanResponse)
async def get_study_plan(topic: str) -> StudyPlanResponse:
    # This endpoint generates a basic study plan around an individual topic using the indexed knowledge.
    plan = rag_service.build_study_plan(topic)
    return StudyPlanResponse(topic=topic, plan=plan)
