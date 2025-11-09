"""Unit tests for RAG Service."""

import pytest
from unittest.mock import Mock, MagicMock
from app.services.rag_service import RAGService
from app.models.document import Document


class TestRAGService:
    """Test suite for RAG Service."""

    @pytest.fixture
    def mock_db(self):
        """Create mock database session."""
        db = Mock()
        db.add = Mock()
        db.commit = Mock()
        db.refresh = Mock()
        db.query = Mock()
        return db

    @pytest.fixture
    def rag_service(self, mock_db):
        """Create RAG service instance with mock DB."""
        return RAGService(mock_db)

    def test_add_document_creates_embedding(self, rag_service, mock_db):
        """Test: Adding document generates 384-dim embedding."""
        # Arrange
        title = "Personalausweis beantragen"
        content = "Gehen Sie zum Bürgerbüro mit Ihrem alten Ausweis."
        category = "verwaltung"

        # Act
        doc = rag_service.add_document(
            title=title,
            content=content,
            category=category
        )

        # Assert
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        assert doc.title == title
        assert doc.content == content
        assert doc.category == category
        # Embedding should be 384 dimensions (paraphrase-multilingual-MiniLM-L12-v2)
        assert len(doc.embedding) == 384

    def test_add_document_with_source(self, rag_service, mock_db):
        """Test: Document with source URL is stored correctly."""
        # Arrange
        source_url = "https://www.ruesselsheim.de/verwaltung/personalausweis"

        # Act
        doc = rag_service.add_document(
            title="Test",
            content="Test content",
            category="test",
            source=source_url
        )

        # Assert
        assert doc.source == source_url

    def test_search_documents_returns_relevant_results(self, rag_service, mock_db):
        """Test: Semantic search finds relevant documents."""
        # Arrange
        query = "Wo beantrage ich einen Personalausweis?"

        # Mock database query result - simulate Row objects
        mock_row1 = Mock()
        mock_row1.id = 1
        mock_row1.title = "Personalausweis beantragen"
        mock_row1.content = "Gehen Sie zum Bürgerbüro mit Ihrem alten Ausweis."
        mock_row1.category = "verwaltung"
        mock_row1.source = "buergerbuero.de"
        mock_row1.doc_metadata = {}
        mock_row1.similarity = 0.85

        mock_row2 = Mock()
        mock_row2.id = 2
        mock_row2.title = "Reisepass beantragen"
        mock_row2.content = "Auch im Bürgerbüro möglich mit Passfoto."
        mock_row2.category = "verwaltung"
        mock_row2.source = "buergerbuero.de"
        mock_row2.doc_metadata = {}
        mock_row2.similarity = 0.72

        # Mock execute to return iterable rows
        mock_db.execute.return_value = [mock_row1, mock_row2]

        # Act
        context = rag_service.get_context_for_query(query, top_k=2)

        # Assert
        assert "Personalausweis" in context
        assert "Bürgerbüro" in context
        mock_db.execute.assert_called_once()

    def test_delete_document_removes_from_db(self, rag_service, mock_db):
        """Test: Deleting document removes it from database."""
        # Arrange
        doc_id = 123
        mock_doc = Mock(spec=Document)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_doc

        # Act
        result = rag_service.delete_document(doc_id)

        # Assert
        assert result is True
        mock_db.delete.assert_called_once_with(mock_doc)
        mock_db.commit.assert_called_once()

    def test_delete_nonexistent_document_returns_false(self, rag_service, mock_db):
        """Test: Deleting non-existent document returns False."""
        # Arrange
        doc_id = 999
        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Act
        result = rag_service.delete_document(doc_id)

        # Assert
        assert result is False
        mock_db.delete.assert_not_called()

    def test_embedding_dimension_is_correct(self, rag_service):
        """Test: Embeddings have correct dimensions (384)."""
        # Arrange
        test_text = "Dies ist ein Test-Text für das Embedding."

        # Act
        embedding = rag_service.embedding_service.create_embedding(test_text)

        # Assert
        assert len(embedding) == 384, f"Expected 384 dimensions, got {len(embedding)}"

    def test_get_all_documents(self, rag_service, mock_db):
        """Test: Retrieving all documents from database."""
        # Arrange
        mock_docs = [
            Mock(id=1, title="Doc 1"),
            Mock(id=2, title="Doc 2"),
            Mock(id=3, title="Doc 3")
        ]
        mock_db.query.return_value.all.return_value = mock_docs

        # Act
        docs = rag_service.get_all_documents()

        # Assert
        assert len(docs) == 3
        assert docs[0].title == "Doc 1"
