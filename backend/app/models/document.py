"""Document model for RAG system."""

from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector
from .base import Base, TimestampMixin


class Document(Base, TimestampMixin):
    """Document model with vector embeddings."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    source = Column(String(500))
    metadata = Column(Text)  # JSON as text
    embedding = Column(Vector(1536))  # OpenAI embeddings dimension

    def __repr__(self) -> str:
        """String representation."""
        return f"<Document(id={self.id}, title='{self.title}', category='{self.category}')>"
