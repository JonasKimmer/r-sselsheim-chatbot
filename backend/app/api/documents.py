"""Document management API endpoints."""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..services import RAGService
from .schemas import DocumentCreate, DocumentResponse, SearchRequest, SearchResult

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/", response_model=DocumentResponse, status_code=201)
async def create_document(
    request: DocumentCreate,
    db: Session = Depends(get_db)
) -> DocumentResponse:
    """Create a new document.

    Args:
        request: Document creation request
        db: Database session

    Returns:
        Created document
    """
    try:
        rag_service = RAGService(db)
        document = rag_service.add_document(
            title=request.title,
            content=request.content,
            category=request.category,
            source=request.source,
            metadata=request.metadata
        )

        return DocumentResponse.model_validate(document)

    except Exception as e:
        logger.error(f"Error creating document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=List[SearchResult])
async def search_documents(
    request: SearchRequest,
    db: Session = Depends(get_db)
) -> List[SearchResult]:
    """Search for similar documents.

    Args:
        request: Search request
        db: Database session

    Returns:
        Search results
    """
    try:
        rag_service = RAGService(db)
        results = rag_service.search_similar_documents(
            query=request.query,
            limit=request.limit,
            category=request.category
        )

        return [SearchResult(**result) for result in results]

    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))
