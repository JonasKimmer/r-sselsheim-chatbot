"""Evaluation service for measuring chatbot performance."""

import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session

from .chat_service import ChatService
from .rag_service import RAGService
from ..models import Document


class EvaluationMetrics:
    """Container for evaluation metrics."""

    def __init__(self):
        self.response_times: List[float] = []
        self.retrieval_scores: List[float] = []
        self.retrieved_doc_counts: List[int] = []
        self.successful_responses: int = 0
        self.failed_responses: int = 0
        self.total_questions: int = 0

    def add_response_time(self, time_ms: float):
        """Add a response time measurement."""
        self.response_times.append(time_ms)

    def add_retrieval_metric(self, score: float, doc_count: int):
        """Add retrieval metrics."""
        self.retrieval_scores.append(score)
        self.retrieved_doc_counts.append(doc_count)

    def add_success(self):
        """Mark a successful response."""
        self.successful_responses += 1
        self.total_questions += 1

    def add_failure(self):
        """Mark a failed response."""
        self.failed_responses += 1
        self.total_questions += 1

    def get_summary(self) -> Dict:
        """Get summary statistics."""
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        avg_retrieval_score = sum(self.retrieval_scores) / len(self.retrieval_scores) if self.retrieval_scores else 0
        avg_doc_count = sum(self.retrieved_doc_counts) / len(self.retrieved_doc_counts) if self.retrieved_doc_counts else 0
        success_rate = (self.successful_responses / self.total_questions * 100) if self.total_questions > 0 else 0

        return {
            "total_questions": self.total_questions,
            "successful_responses": self.successful_responses,
            "failed_responses": self.failed_responses,
            "success_rate_percent": round(success_rate, 2),
            "avg_response_time_ms": round(avg_response_time, 2),
            "min_response_time_ms": round(min(self.response_times), 2) if self.response_times else 0,
            "max_response_time_ms": round(max(self.response_times), 2) if self.response_times else 0,
            "avg_retrieval_score": round(avg_retrieval_score, 4),
            "avg_documents_retrieved": round(avg_doc_count, 2)
        }


class EvaluationService:
    """Service for evaluating chatbot performance."""

    def __init__(self, db: Session):
        self.db = db
        self.chat_service = ChatService(db)
        self.rag_service = RAGService(db)

    async def evaluate_question(
        self,
        question: str,
        expected_category: Optional[str] = None
    ) -> Dict:
        """
        Evaluate a single question and return metrics.

        Args:
            question: The question to evaluate
            expected_category: Optional expected document category

        Returns:
            Dictionary with metrics for this question
        """
        start_time = time.time()

        try:
            # Search for relevant documents
            search_start = time.time()
            relevant_docs = self.rag_service.search(question, limit=3)
            search_time = (time.time() - search_start) * 1000

            # Generate response
            response_start = time.time()
            response = await self.chat_service.get_response(
                session_id=f"eval_{int(time.time())}",
                message=question
            )
            generation_time = (time.time() - response_start) * 1000

            total_time = (time.time() - start_time) * 1000

            # Calculate retrieval metrics
            retrieval_score = relevant_docs[0]["score"] if relevant_docs else 0.0
            doc_count = len(relevant_docs)

            # Check if correct category was retrieved
            category_match = False
            if expected_category and relevant_docs:
                category_match = any(
                    doc.get("category") == expected_category
                    for doc in relevant_docs
                )

            return {
                "success": True,
                "question": question,
                "response_length": len(response),
                "total_time_ms": round(total_time, 2),
                "search_time_ms": round(search_time, 2),
                "generation_time_ms": round(generation_time, 2),
                "retrieval_score": round(retrieval_score, 4),
                "documents_retrieved": doc_count,
                "category_match": category_match,
                "retrieved_docs": [
                    {
                        "title": doc.get("title", ""),
                        "score": round(doc.get("score", 0.0), 4),
                        "category": doc.get("category", "")
                    }
                    for doc in relevant_docs
                ]
            }

        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "question": question,
                "error": str(e),
                "total_time_ms": round(total_time, 2)
            }

    async def evaluate_batch(
        self,
        test_questions: List[Dict[str, str]]
    ) -> Dict:
        """
        Evaluate a batch of questions.

        Args:
            test_questions: List of dicts with 'question' and optional 'category'

        Returns:
            Summary metrics and detailed results
        """
        metrics = EvaluationMetrics()
        detailed_results = []

        for test_case in test_questions:
            question = test_case.get("question", "")
            expected_category = test_case.get("category")

            result = await self.evaluate_question(question, expected_category)
            detailed_results.append(result)

            if result["success"]:
                metrics.add_success()
                metrics.add_response_time(result["total_time_ms"])
                metrics.add_retrieval_metric(
                    result["retrieval_score"],
                    result["documents_retrieved"]
                )
            else:
                metrics.add_failure()

        return {
            "summary": metrics.get_summary(),
            "detailed_results": detailed_results,
            "timestamp": datetime.now().isoformat()
        }

    def get_rag_statistics(self) -> Dict:
        """Get statistics about the RAG database."""
        total_docs = self.db.query(Document).count()

        # Count documents by category
        from sqlalchemy import func
        category_counts = (
            self.db.query(Document.category, func.count(Document.id))
            .group_by(Document.category)
            .all()
        )

        return {
            "total_documents": total_docs,
            "documents_by_category": {
                category: count for category, count in category_counts
            },
            "embedding_dimension": 384  # paraphrase-multilingual-MiniLM-L12-v2
        }
