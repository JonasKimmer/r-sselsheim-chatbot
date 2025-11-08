"""Chat models for conversation management."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from .base import Base, TimestampMixin


class MessageRole(str, enum.Enum):
    """Message role enumeration."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatSession(Base, TimestampMixin):
    """Chat session model."""

    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    user_identifier = Column(String(200))  # Optional user ID or IP
    title = Column(String(500))
    is_active = Column(Integer, default=1)  # 1 = active, 0 = archived

    # Relationship
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """String representation."""
        return f"<ChatSession(id={self.id}, session_id='{self.session_id}')>"


class ChatMessage(Base, TimestampMixin):
    """Chat message model."""

    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False, index=True)
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    context_used = Column(Text)  # Retrieved context for this message

    # Relationship
    session = relationship("ChatSession", back_populates="messages")

    def __repr__(self) -> str:
        """String representation."""
        return f"<ChatMessage(id={self.id}, role={self.role}, session_id={self.session_id})>"
