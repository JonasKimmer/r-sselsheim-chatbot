"""Load testing with Locust.

Run with:
    locust -f tests/locustfile.py --host=http://localhost:8000

Then open browser at http://localhost:8089 to start the load test.
"""

from locust import HttpUser, task, between
import random
import string


class ChatbotUser(HttpUser):
    """Simulated chatbot user for load testing."""

    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks

    def on_start(self):
        """Initialize user session."""
        # Generate random session ID
        self.session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        # Sample questions for testing
        self.questions = [
            "Wie ist das Wetter heute?",
            "Wo ist das Rathaus?",
            "Gibt es Blitzer in Rüsselsheim?",
            "Wann ist der nächste Feiertag?",
            "Wie beantrage ich einen Personalausweis?",
            "Was sind die Öffnungszeiten des Bürgerbüros?",
            "Wo kann ich günstig tanken?",
            "Wann wird die Mülltonne geleert?",
            "Gibt es Restaurants in der Nähe?",
            "Wie komme ich zum Hauptbahnhof?"
        ]

    @task(10)
    def send_chat_message(self):
        """Send a chat message (most common task)."""
        message = random.choice(self.questions)

        response = self.client.post(
            "/api/chat/",
            json={
                "session_id": self.session_id,
                "message": message
            },
            name="/api/chat/"
        )

        if response.status_code == 200:
            # Verify response structure
            data = response.json()
            assert "answer" in data
            assert "session_id" in data
        else:
            response.failure(f"Status code: {response.status_code}")

    @task(3)
    def get_chat_history(self):
        """Get chat history (less common)."""
        response = self.client.get(
            f"/api/chat/{self.session_id}/history",
            name="/api/chat/{session_id}/history"
        )

        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
        else:
            response.failure(f"Status code: {response.status_code}")

    @task(2)
    def get_weather(self):
        """Get weather information."""
        response = self.client.get(
            "/api/weather/",
            name="/api/weather/"
        )

        if response.status_code == 200:
            data = response.json()
            assert "current" in data
        else:
            response.failure(f"Status code: {response.status_code}")

    @task(2)
    def geocode_address(self):
        """Geocode an address."""
        addresses = [
            "Rathaus Rüsselsheim",
            "Opelkreisel Rüsselsheim",
            "Hauptbahnhof Rüsselsheim",
            "Main-Taunus-Zentrum"
        ]

        address = random.choice(addresses)

        response = self.client.get(
            f"/api/maps/geocode?address={address}",
            name="/api/maps/geocode"
        )

        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
        else:
            response.failure(f"Status code: {response.status_code}")

    @task(1)
    def get_speed_cameras(self):
        """Get speed camera information."""
        response = self.client.get(
            "/api/traffic/speed-cameras",
            name="/api/traffic/speed-cameras"
        )

        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
        else:
            response.failure(f"Status code: {response.status_code}")

    @task(1)
    def get_health(self):
        """Check API health."""
        response = self.client.get(
            "/api/health",
            name="/api/health"
        )

        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "healthy"
        else:
            response.failure(f"Status code: {response.status_code}")

    @task(1)
    def get_monitoring_metrics(self):
        """Get monitoring metrics."""
        response = self.client.get(
            "/api/monitoring/health",
            name="/api/monitoring/health"
        )

        if response.status_code == 200:
            data = response.json()
            assert "status" in data
        else:
            response.failure(f"Status code: {response.status_code}")


class StressTestUser(HttpUser):
    """User for stress testing with high load."""

    wait_time = between(0.1, 0.5)  # Very short wait times

    def on_start(self):
        """Initialize user session."""
        self.session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    @task
    def rapid_fire_requests(self):
        """Send rapid requests to stress test the API."""
        endpoints = [
            "/api/health",
            "/api/weather/",
            "/api/traffic/speed-cameras",
            "/api/monitoring/health"
        ]

        endpoint = random.choice(endpoints)
        self.client.get(endpoint, name="stress-test-endpoint")
