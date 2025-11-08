"""Application configuration."""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Database
    postgres_user: str = "ruesselsheim_bot"
    postgres_password: str = "change_me_in_production"
    postgres_db: str = "ruesselsheim_chatbot"
    database_url: str = "postgresql://ruesselsheim_bot:change_me_in_production@postgres:5432/ruesselsheim_chatbot"

    # LLM Provider Configuration
    llm_provider: str = "ollama"  # "ollama" (free, local), "gemini" (free), or "claude" (paid)

    # Anthropic API (only needed if llm_provider = "claude")
    anthropic_api_key: str = ""

    # Google Gemini API (only needed if llm_provider = "gemini")
    gemini_api_key: str = ""

    # Ollama Configuration (only needed if llm_provider = "ollama")
    ollama_host: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.1:8b"  # or llama3.2:3b (faster), llama3.1:70b (better quality)

    # OpenAI API (optional - only needed if using OpenAI embeddings)
    openai_api_key: str = ""

    # Application
    environment: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # Embeddings Configuration
    embedding_provider: str = "local"  # "local" or "openai"
    # For OpenAI embeddings:
    openai_embedding_model: str = "text-embedding-3-small"
    openai_embedding_dim: int = 1536
    # For local embeddings:
    local_embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2"
    local_embedding_dim: int = 384

    # Vector DB
    chunk_size: int = 1000
    chunk_overlap: int = 200

    @property
    def embedding_dimension(self) -> int:
        """Get current embedding dimension based on provider."""
        if self.embedding_provider == "openai":
            return self.openai_embedding_dim
        return self.local_embedding_dim

    # LLM Model Configuration
    # For Claude:
    claude_model: str = "claude-3-5-sonnet-20241022"
    # For Gemini (google-generativeai >= 0.8.0):
    gemini_model: str = "gemini-1.5-flash"  # free tier: gemini-1.5-flash or gemini-1.5-pro

    # Common settings
    max_tokens: int = 4096
    temperature: float = 0.7

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins as list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
