"""API endpoints for evaluation and metrics."""

from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..services.evaluation_service import EvaluationService
from ..evaluation.test_questions import (
    TEST_QUESTIONS,
    get_all_test_cases,
    get_questions_by_category
)

router = APIRouter(
    prefix="/api/evaluation",
    tags=["evaluation"]
)


class QuestionRequest(BaseModel):
    """Request model for single question evaluation."""
    question: str
    expected_category: Optional[str] = None


class BatchEvaluationRequest(BaseModel):
    """Request model for batch evaluation."""
    questions: List[Dict[str, str]]


@router.get("/test-questions")
async def get_test_questions(
    category: Optional[str] = Query(None, description="Filter by category")
) -> Dict:
    """
    Get the test questions dataset.

    Args:
        category: Optional category filter

    Returns:
        Test questions with metadata
    """
    if category:
        questions = get_questions_by_category(category)
        return {
            "category": category,
            "count": len(questions),
            "questions": questions
        }

    return {
        "total": len(TEST_QUESTIONS),
        "categories": list(set(q["category"] for q in TEST_QUESTIONS)),
        "questions": TEST_QUESTIONS
    }


@router.post("/evaluate/single")
async def evaluate_single_question(
    request: QuestionRequest,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Evaluate a single question and return metrics.

    Args:
        request: Question and optional expected category
        db: Database session

    Returns:
        Evaluation metrics for the question
    """
    service = EvaluationService(db)

    try:
        result = await service.evaluate_question(
            request.question,
            request.expected_category
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluate/batch")
async def evaluate_batch(
    request: Optional[BatchEvaluationRequest] = None,
    db: Session = Depends(get_db)
) -> Dict:
    """
    Evaluate a batch of questions.

    If no request body is provided, uses the default test dataset.

    Args:
        request: Optional custom question list
        db: Database session

    Returns:
        Summary metrics and detailed results
    """
    service = EvaluationService(db)

    # Use default test questions if none provided
    test_questions = request.questions if request else get_all_test_cases()

    try:
        results = await service.evaluate_batch(test_questions)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rag/statistics")
async def get_rag_statistics(
    db: Session = Depends(get_db)
) -> Dict:
    """
    Get statistics about the RAG database.

    Returns:
        Document counts by category and other RAG metrics
    """
    service = EvaluationService(db)

    try:
        stats = service.get_rag_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def evaluation_health() -> Dict:
    """Health check for evaluation endpoints."""
    return {
        "status": "healthy",
        "test_questions_loaded": len(TEST_QUESTIONS),
        "categories": list(set(q["category"] for q in TEST_QUESTIONS))
    }
