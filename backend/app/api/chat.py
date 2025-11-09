"""Chat API endpoints."""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..config import get_settings
from .schemas import ChatRequest, ChatResponse, ChatHistoryResponse
from ..middleware.security import InputValidator

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
        # Validate and sanitize inputs
        session_id = InputValidator.validate_session_id(request.session_id) if request.session_id else ""
        message = InputValidator.sanitize_text(request.message, max_length=5000)

        chat_service = get_chat_service(db)

        result = await chat_service.chat(
            session_id=session_id,
            message=message
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
        # Validate session ID
        validated_session_id = InputValidator.validate_session_id(session_id)

        chat_service = get_chat_service(db)
        messages = chat_service.get_session_history(validated_session_id)

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
