"""Chat service using Google Gemini (free tier available)."""

import logging
import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import google.generativeai as genai
from ..models.chat import ChatSession, ChatMessage, MessageRole
from .rag_service import RAGService
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class GeminiChatService:
    """Service for chat operations using Google Gemini."""

    SYSTEM_PROMPT = """Du bist ein hilfreicher Assistent für die Stadt Rüsselsheim am Main.

Deine Aufgaben:
- Beantworte Fragen zu städtischen Dienstleistungen, Öffnungszeiten und Verfahren
- Erkenne die Absicht des Benutzers (Information, Terminvereinbarung, Formulare)
- Sei höflich, präzise und verwende die bereitgestellten Informationen
- Wenn du etwas nicht weißt, gib das ehrlich zu und verweise auf die entsprechende Stelle

Kategorien:
- Bürgerservice: Personalausweis, Meldewesen, etc.
- KFZ-Zulassung: Anmeldung, Ummeldung, Abmeldung
- Abfallwirtschaft: Müllabfuhr, Sperrmüll, Recycling
- Termine: Terminvereinbarungen
- Allgemein: Öffnungszeiten, Kontakte, Standorte

Antworte auf Deutsch und sei präzise."""

    def __init__(self, db: Session):
        """Initialize chat service with Gemini.

        Args:
            db: Database session
        """
        self.db = db
        genai.configure(api_key=settings.gemini_api_key)

        # Configure Gemini model
        generation_config = {
            "temperature": settings.temperature,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": settings.max_tokens,
        }

        self.model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            generation_config=generation_config,
            system_instruction=self.SYSTEM_PROMPT
        )

        self.rag_service = RAGService(db)

    def create_session(self, user_identifier: Optional[str] = None) -> ChatSession:
        """Create a new chat session.

        Args:
            user_identifier: Optional user identifier

        Returns:
            Created chat session
        """
        try:
            session = ChatSession(
                session_id=str(uuid.uuid4()),
                user_identifier=user_identifier,
                is_active=1
            )
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)

            logger.info(f"Created chat session: {session.session_id}")
            return session

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating session: {e}")
            raise

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID.

        Args:
            session_id: Session ID

        Returns:
            Chat session or None
        """
        return self.db.query(ChatSession).filter(
            ChatSession.session_id == session_id
        ).first()

    def get_session_history(self, session_id: str, limit: int = 20) -> List[ChatMessage]:
        """Get chat history for a session.

        Args:
            session_id: Session ID
            limit: Maximum number of messages

        Returns:
            List of chat messages
        """
        session = self.get_session(session_id)
        if not session:
            return []

        return self.db.query(ChatMessage).filter(
            ChatMessage.session_id == session.id
        ).order_by(ChatMessage.created_at.desc()).limit(limit).all()

    def detect_intent(self, message: str) -> str:
        """Detect user intent from message.

        Args:
            message: User message

        Returns:
            Detected intent
        """
        message_lower = message.lower()

        # Simple keyword-based intent detection
        if any(word in message_lower for word in ["termin", "vereinbaren", "anmeldung"]):
            return "appointment"
        elif any(word in message_lower for word in ["formular", "antrag", "download"]):
            return "form"
        else:
            return "information"

    def chat(
        self,
        session_id: str,
        message: str
    ) -> Dict[str, Any]:
        """Process a chat message using Gemini.

        Args:
            session_id: Session ID
            message: User message

        Returns:
            Response with answer and metadata
        """
        try:
            # Get or create session
            session = self.get_session(session_id)
            if not session:
                session = self.create_session()
                session_id = session.session_id

            # Detect intent
            intent = self.detect_intent(message)

            # Get relevant context from RAG
            context = self.rag_service.get_context_for_query(message)

            # Get conversation history
            history = self.get_session_history(session_id)
            history.reverse()  # Chronological order

            # Build chat history for Gemini
            chat_history = []
            for msg in history[-10:]:  # Last 10 messages
                role = "user" if msg.role == MessageRole.USER else "model"
                chat_history.append({
                    "role": role,
                    "parts": [msg.content]
                })

            # Create chat session with history
            chat = self.model.start_chat(history=chat_history)

            # Build user message with context
            user_message = message
            if context:
                user_message = f"""Kontext aus der Wissensdatenbank:
{context}

---
Benutzerfrage: {message}"""

            # Get response from Gemini
            response = chat.send_message(user_message)
            assistant_message = response.text

            # Save user message
            user_msg = ChatMessage(
                session_id=session.id,
                role=MessageRole.USER,
                content=message,
                context_used=None
            )
            self.db.add(user_msg)

            # Save assistant message
            assistant_msg = ChatMessage(
                session_id=session.id,
                role=MessageRole.ASSISTANT,
                content=assistant_message,
                context_used=context if context else None
            )
            self.db.add(assistant_msg)

            # Update session title if first message
            if not session.title:
                session.title = message[:100]

            self.db.commit()

            logger.info(f"Chat response generated for session: {session_id}")

            return {
                "session_id": session_id,
                "message": assistant_message,
                "intent": intent,
                "context_used": bool(context)
            }

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error in chat: {e}")
            raise
