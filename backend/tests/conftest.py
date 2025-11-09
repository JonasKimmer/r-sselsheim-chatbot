"""Pytest configuration and fixtures."""

import pytest
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set test environment variables
os.environ["ENVIRONMENT"] = "test"
# Use PostgreSQL from docker-compose (not SQLite)
# DATABASE_URL is already set by docker-compose.yml
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["EMBEDDING_PROVIDER"] = "local"


@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration."""
    return {
        "llm_provider": "ollama",
        "embedding_provider": "local",
        "environment": "test"
    }


@pytest.fixture
def sample_document_data():
    """Provide sample document data for testing."""
    return {
        "title": "Personalausweis beantragen",
        "content": "Um einen Personalausweis zu beantragen, gehen Sie zum Bürgerbüro im Rathaus. "
                   "Bringen Sie Ihren alten Ausweis und ein biometrisches Passfoto mit.",
        "category": "verwaltung",
        "source": "https://www.ruesselsheim.de/verwaltung/personalausweis"
    }


@pytest.fixture
def sample_weather_queries():
    """Provide sample weather-related queries."""
    return [
        "Wie ist das Wetter?",
        "Wetter heute",
        "Regnet es morgen?",
        "Temperatur in Rüsselsheim",
        "Wie warm wird es?"
    ]


@pytest.fixture
def sample_location_queries():
    """Provide sample location-related queries."""
    return [
        "Wo liegt das Restaurant 3h's?",
        "Wo ist der Opelkreisel?",
        "Wo finde ich das Bürgerbüro?",
        "Adresse vom Rathaus"
    ]


@pytest.fixture
def ruesselsheim_coordinates():
    """Provide Rüsselsheim coordinates."""
    return {
        "lat": 49.9897,
        "lon": 8.4189
    }
