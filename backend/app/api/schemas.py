"""Pydantic schemas for API requests/responses."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Chat schemas
class ChatRequest(BaseModel):
    """Chat request schema."""

    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    session_id: Optional[str] = Field(None, description="Optional session ID")


class ChatResponse(BaseModel):
    """Chat response schema."""

    session_id: str
    message: str
    intent: str
    context_used: bool


class ChatHistoryResponse(BaseModel):
    """Chat history response schema."""

    role: str
    content: str
    created_at: datetime


# Document schemas
class DocumentCreate(BaseModel):
    """Document creation schema."""

    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=100)
    source: Optional[str] = Field(None, max_length=500)
    doc_metadata: Optional[str] = None


class DocumentResponse(BaseModel):
    """Document response schema."""

    id: int
    title: str
    content: str
    category: str
    source: Optional[str]
    created_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True


class SearchRequest(BaseModel):
    """Search request schema."""

    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(5, ge=1, le=20)
    category: Optional[str] = None


class SearchResult(BaseModel):
    """Search result schema."""

    id: int
    title: str
    content: str
    category: str
    similarity: float


# Health check
class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    database: str
    version: str
