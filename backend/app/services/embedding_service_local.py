"""Local embedding service using Sentence Transformers (no API key needed)."""

import logging
from typing import List
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class LocalEmbeddingService:
    """Service for generating text embeddings locally using Sentence Transformers."""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        """Initialize local embedding model.

        Args:
            model_name: Name of the sentence-transformers model
                       Default: paraphrase-multilingual-MiniLM-L12-v2 (supports German)
                       Alternatives:
                       - "paraphrase-multilingual-mpnet-base-v2" (better quality, slower)
                       - "distiluse-base-multilingual-cased-v2"
        """
        logger.info(f"Loading local embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        logger.info(f"Model loaded. Embedding dimension: {self.embedding_dim}")

    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            raise

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Error creating embeddings: {e}")
            raise
