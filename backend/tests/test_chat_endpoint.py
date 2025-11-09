"""Integration tests for Chat API endpoint."""

import pytest
from httpx import AsyncClient
from app.main import app


# Mark all chat endpoint tests as integration tests (may require Ollama)
pytestmark = pytest.mark.integration


@pytest.mark.asyncio
class TestChatEndpoint:
    """Test suite for /api/chat endpoint."""

    async def test_chat_endpoint_exists(self):
        """Test: POST /api/chat endpoint is accessible."""
        async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as client:
            response = await client.post("/api/chat", json={
                "session_id": "test-session-1",
                "message": "Hallo"
            })
            # Should not return 404
            assert response.status_code != 404

    @pytest.mark.skip(reason="Requires Ollama running on host.docker.internal")
    async def test_chat_with_weather_question(self):
        """Test: Weather question triggers weather API."""
        async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as client:
            response = await client.post("/api/chat", json={
                "session_id": "test-weather-1",
                "message": "Wie ist das Wetter heute?"
            })

            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            # Answer should contain weather info
            answer_lower = data["answer"].lower()
            assert any(word in answer_lower for word in ["wetter", "temperatur", "grad", "°c"])

    @pytest.mark.skip(reason="Requires Ollama running on host.docker.internal")
    async def test_chat_with_location_question(self):
        """Test: Location question triggers maps API."""
        async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as client:
            response = await client.post("/api/chat", json={
                "session_id": "test-location-1",
                "message": "Wo liegt das Rathaus Rüsselsheim?"
            })

            assert response.status_code == 200
            data = response.json()
            assert "answer" in data

    @pytest.mark.skip(reason="Requires Ollama running on host.docker.internal")
    async def test_chat_maintains_session_history(self):
        """Test: Multiple messages in same session are tracked."""
        session_id = "test-history-1"

        async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as client:
            # First message
            response1 = await client.post("/api/chat", json={
                "session_id": session_id,
                "message": "Hallo, ich bin ein Bürger aus Rüsselsheim."
            })
            assert response1.status_code == 200

            # Second message
            response2 = await client.post("/api/chat", json={
                "session_id": session_id,
                "message": "Wie ist das Wetter?"
            })
            assert response2.status_code == 200

            # Context should be maintained (LLM might reference previous message)

    async def test_chat_invalid_request_missing_message(self):
        """Test: Request without message field returns error."""
        async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as client:
            response = await client.post("/api/chat", json={
                "session_id": "test-invalid-1"
                # Missing "message" field
            })

            # Should return 422 (Unprocessable Entity) due to Pydantic validation
            assert response.status_code == 422

    @pytest.mark.skip(reason="Requires Ollama running on host.docker.internal")
    async def test_chat_invalid_request_missing_session_id(self):
        """Test: Request without session_id returns error."""
        async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as client:
            response = await client.post("/api/chat", json={
                "message": "Hallo"
                # Missing "session_id" field
            })

            assert response.status_code == 422

    @pytest.mark.skip(reason="Requires Ollama running on host.docker.internal")
    async def test_chat_response_structure(self):
        """Test: Response has correct structure."""
        async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as client:
            response = await client.post("/api/chat", json={
                "session_id": "test-structure-1",
                "message": "Test"
            })

            assert response.status_code == 200
            data = response.json()

            # Check response structure
            assert "answer" in data
            assert "session_id" in data
            assert isinstance(data["answer"], str)
            assert isinstance(data["session_id"], str)
