"""RAG (Retrieval Augmented Generation) service."""

import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..models.document import Document
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class RAGService:
    """Service for RAG operations."""

    def __init__(self, db: Session):
        """Initialize RAG service.

        Args:
            db: Database session
        """
        self.db = db

        # Choose embedding service based on configuration
        if settings.embedding_provider == "openai":
            from .embedding_service import EmbeddingService
            self.embedding_service = EmbeddingService()
            logger.info("Using OpenAI embeddings")
        else:
            from .embedding_service_local import LocalEmbeddingService
            self.embedding_service = LocalEmbeddingService(settings.local_embedding_model)
            logger.info("Using local embeddings")

    def add_document(
        self,
        title: str,
        content: str,
        category: str,
        source: Optional[str] = None,
        metadata: Optional[str] = None
    ) -> Document:
        """Add a document to the vector database.

        Args:
            title: Document title
            content: Document content
            category: Document category
            source: Document source
            metadata: Additional metadata as JSON string

        Returns:
            Created document
        """
        try:
            # Generate embedding
            embedding = self.embedding_service.create_embedding(content)

            # Create document
            document = Document(
                title=title,
                content=content,
                category=category,
                source=source,
                metadata=metadata,
                embedding=embedding
            )

            self.db.add(document)
            self.db.commit()
            self.db.refresh(document)

            logger.info(f"Document added: {title}")
            return document

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error adding document: {e}")
            raise

    def search_similar_documents(
        self,
        query: str,
        limit: int = 5,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents using semantic search.

        Args:
            query: Search query
            limit: Maximum number of results
            category: Optional category filter

        Returns:
            List of similar documents with similarity scores
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_service.create_embedding(query)

            # Build SQL query with vector similarity
            sql = text("""
                SELECT
                    id,
                    title,
                    content,
                    category,
                    source,
                    metadata,
                    1 - (embedding <=> :query_embedding) as similarity
                FROM documents
                WHERE (:category IS NULL OR category = :category)
                ORDER BY embedding <=> :query_embedding
                LIMIT :limit
            """)

            # Execute query
            result = self.db.execute(
                sql,
                {
                    "query_embedding": str(query_embedding),
                    "category": category,
                    "limit": limit
                }
            )

            # Format results
            documents = []
            for row in result:
                documents.append({
                    "id": row.id,
                    "title": row.title,
                    "content": row.content,
                    "category": row.category,
                    "source": row.source,
                    "metadata": row.metadata,
                    "similarity": float(row.similarity)
                })

            logger.info(f"Found {len(documents)} similar documents for query: {query[:50]}...")
            return documents

        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            raise

    def get_context_for_query(
        self,
        query: str,
        max_context_length: int = 3000
    ) -> str:
        """Get relevant context for a query.

        Args:
            query: User query
            max_context_length: Maximum context length in characters

        Returns:
            Formatted context string
        """
        try:
            documents = self.search_similar_documents(query, limit=5)

            if not documents:
                return ""

            context_parts = []
            current_length = 0

            for doc in documents:
                doc_text = f"[{doc['category']}] {doc['title']}\n{doc['content']}\n"
                doc_length = len(doc_text)

                if current_length + doc_length > max_context_length:
                    break

                context_parts.append(doc_text)
                current_length += doc_length

            context = "\n---\n".join(context_parts)
            logger.info(f"Generated context of {len(context)} characters")
            return context

        except Exception as e:
            logger.error(f"Error getting context: {e}")
            return ""
