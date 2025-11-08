"""Chat API endpoints."""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..config import get_settings
from .schemas import ChatRequest, ChatResponse, ChatHistoryResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chat", tags=["chat"])
settings = get_settings()


def get_chat_service(db: Session):
    """Get the appropriate chat service based on configuration."""
    if settings.llm_provider == "gemini":
        from ..services.chat_service_gemini import GeminiChatService
        return GeminiChatService(db)
    elif settings.llm_provider == "ollama":
        from ..services.chat_service_ollama import OllamaChatService
        return OllamaChatService(db)
    else:
        from ..services.chat_service import ChatService
        return ChatService(db)


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
) -> ChatResponse:
    """Process a chat message.

    Args:
        request: Chat request
        db: Database session

    Returns:
        Chat response
    """
    try:
        chat_service = get_chat_service(db)

        # Use provided session_id or create new session
        session_id = request.session_id or ""

        result = await chat_service.chat(
            session_id=session_id,
            message=request.message
        )

        return ChatResponse(**result)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/history", response_model=List[ChatHistoryResponse])
async def get_history(
    session_id: str,
    db: Session = Depends(get_db)
) -> List[ChatHistoryResponse]:
    """Get chat history for a session.

    Args:
        session_id: Session ID
        db: Database session

    Returns:
        Chat history
    """
    try:
        chat_service = get_chat_service(db)
        messages = chat_service.get_session_history(session_id)

        return [
            ChatHistoryResponse(
                role=msg.role.value,
                content=msg.content,
                created_at=msg.created_at
            )
            for msg in reversed(messages)
        ]

    except Exception as e:
        logger.error(f"Error getting chat history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
