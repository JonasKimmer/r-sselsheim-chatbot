"""Document model for RAG system."""

from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector
from .base import Base, TimestampMixin


class Document(Base, TimestampMixin):
    """Document model with vector embeddings.

    Note: The embedding dimension is set to 384 by default (for local embeddings).
    If using OpenAI embeddings (1536 dimensions), you need to:
    1. Drop the existing documents table
    2. Change the dimension below to 1536
    3. Recreate the tables
    """

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    source = Column(String(500))
    metadata = Column(Text)  # JSON as text
    embedding = Column(Vector(384))  # Default: local embeddings (384 dim)
                                      # For OpenAI: change to 1536

    def __repr__(self) -> str:
        """String representation."""
        return f"<Document(id={self.id}, title='{self.title}', category='{self.category}')>"
