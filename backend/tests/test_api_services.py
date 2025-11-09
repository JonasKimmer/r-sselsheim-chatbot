"""Integration tests for API services (weather, maps, traffic, etc.)."""

import pytest
from app.services import weather_service, maps_service, traffic_service
from app.services import holidays_service, api_helper


class TestWeatherService:
    """Tests for Weather Service (Open-Meteo API)."""

    @pytest.mark.asyncio
    async def test_get_weather_for_ruesselsheim(self):
        """Test: Weather API returns data for Rüsselsheim."""
        # Act
        result = await weather_service.get_weather()

        # Assert
        assert result is not None
        assert "current_weather" in result or "current" in result
        # Default coordinates should be Rüsselsheim

    @pytest.mark.asyncio
    async def test_get_weather_with_custom_coordinates(self):
        """Test: Weather API accepts custom lat/lon."""
        # Arrange - Frankfurt coordinates
        lat, lon = 50.1109, 8.6821

        # Act
        result = await weather_service.get_weather(lat=lat, lon=lon)

        # Assert
        assert result is not None

    @pytest.mark.asyncio
    async def test_get_weather_formats_response(self):
        """Test: Weather data is properly formatted."""
        # Act
        weather_str = await weather_service.get_weather_info()

        # Assert - should contain German weather info
        assert isinstance(weather_str, str)
        assert len(weather_str) > 0


class TestMapsService:
    """Tests for Maps Service (Nominatim/OSM)."""

    @pytest.mark.asyncio
    async def test_geocode_ruesselsheim(self):
        """Test: Geocoding 'Rüsselsheim' returns coordinates."""
        # Act
        results = await maps_service.geocode_address("Rüsselsheim")

        # Assert
        assert len(results) > 0
        first_result = results[0]
        assert "lat" in first_result
        assert "lon" in first_result
        # Should be near Rüsselsheim (49.99, 8.41)
        assert 49.9 < float(first_result["lat"]) < 50.1
        assert 8.3 < float(first_result["lon"]) < 8.5

    @pytest.mark.asyncio
    async def test_reverse_geocode(self):
        """Test: Reverse geocoding returns address."""
        # Arrange - Rüsselsheim coordinates
        lat, lon = 49.9897, 8.4189

        # Act
        result = await maps_service.reverse_geocode(lat, lon)

        # Assert
        assert result is not None
        assert "display_name" in result
        assert "Rüsselsheim" in result["display_name"] or "Rüsselsheim" in str(result)

    @pytest.mark.asyncio
    async def test_search_nearby_restaurants(self):
        """Test: Nearby search finds restaurants."""
        # Arrange
        lat, lon = 49.9897, 8.4189
        query = "restaurant"

        # Act
        results = await maps_service.search_nearby(lat, lon, query)

        # Assert
        assert isinstance(results, list)
        # Note: Results may vary, so we just check format
        if len(results) > 0:
            assert "name" in results[0] or "display_name" in results[0]


class TestTrafficService:
    """Tests for Traffic Service (Speed Cameras)."""

    @pytest.mark.asyncio
    async def test_get_all_speed_cameras(self):
        """Test: Returns all speed cameras in database."""
        # Act
        cameras = await traffic_service.get_speed_cameras()

        # Assert
        assert len(cameras) > 0
        # Should have at least 6 cameras (as in SPEED_CAMERAS list)
        assert len(cameras) >= 6

    @pytest.mark.asyncio
    async def test_speed_camera_has_required_fields(self):
        """Test: Each camera has required fields."""
        # Act
        cameras = await traffic_service.get_speed_cameras()

        # Assert
        first_camera = cameras[0]
        assert "id" in first_camera
        assert "name" in first_camera
        assert "latitude" in first_camera
        assert "longitude" in first_camera
        assert "street" in first_camera
        assert "type" in first_camera
        assert "speed_limit" in first_camera

    @pytest.mark.asyncio
    async def test_get_nearby_speed_cameras(self):
        """Test: Filter cameras by distance."""
        # Arrange - Rüsselsheim coordinates
        lat, lon = 49.9897, 8.4189
        radius = 5000  # 5km

        # Act
        cameras = await traffic_service.get_speed_cameras(lat, lon, radius)

        # Assert
        assert isinstance(cameras, list)
        # All cameras should have distance_meters field
        if len(cameras) > 0:
            assert "distance_meters" in cameras[0]
            # Should be sorted by distance (closest first)
            distances = [c["distance_meters"] for c in cameras]
            assert distances == sorted(distances)

    @pytest.mark.asyncio
    async def test_get_speed_camera_by_id(self):
        """Test: Retrieve specific camera by ID."""
        # Arrange
        camera_id = 1  # B43 Rüsselsheim Richtung Mainz

        # Act
        camera = await traffic_service.get_speed_camera_by_id(camera_id)

        # Assert
        assert camera is not None
        assert camera["id"] == camera_id
        assert "B43" in camera["name"]


class TestHolidaysService:
    """Tests for Holidays Service (feiertage-api.de)."""

    @pytest.mark.asyncio
    async def test_get_holidays_for_current_year(self):
        """Test: Returns holidays for current year."""
        # Act
        result = await holidays_service.get_holidays()

        # Assert
        assert isinstance(result, str)
        assert len(result) > 0
        # Should mention Hessen
        assert "Hessen" in result or "HE" in result

    @pytest.mark.asyncio
    async def test_is_today_holiday(self):
        """Test: Checks if today is a holiday."""
        # Act
        result = await holidays_service.is_holiday_today()

        # Assert
        assert isinstance(result, str)
        # Should either say "Heute ist..." or "Heute ist kein Feiertag"
        assert "heute" in result.lower() or "Heute" in result

    @pytest.mark.asyncio
    async def test_get_next_holiday(self):
        """Test: Returns next upcoming holiday."""
        # Act
        result = await holidays_service.get_next_holiday()

        # Assert
        assert isinstance(result, str)
        assert len(result) > 0
        # Should mention a date or month
        assert any(month in result for month in ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"])


class TestAPIHelper:
    """Tests for API Helper (Intent Detection)."""

    def test_detect_weather_intent(self):
        """Test: 'Wie ist das Wetter?' → weather"""
        # Arrange
        messages = [
            "Wie ist das Wetter?",
            "Wetter heute",
            "Regnet es morgen?",
            "Temperatur in Rüsselsheim"
        ]

        # Act & Assert
        for msg in messages:
            intent = api_helper.detect_api_intent(msg)
            assert intent == "weather", f"Failed for: {msg}"

    def test_detect_location_intent(self):
        """Test: 'Wo liegt...' → location"""
        # Arrange
        messages = [
            "Wo liegt das Restaurant 3h's?",
            "Wo ist der Opelkreisel?",
            "Wo finde ich das Bürgerbüro?"
        ]

        # Act & Assert
        for msg in messages:
            intent = api_helper.detect_api_intent(msg)
            assert intent == "location", f"Failed for: {msg}"

    def test_detect_traffic_intent(self):
        """Test: 'Blitzer' → traffic"""
        # Arrange
        messages = [
            "Wo sind Blitzer?",
            "Blitzer auf der B43",
            "Gibt es Radarkontrollen?"
        ]

        # Act & Assert
        for msg in messages:
            intent = api_helper.detect_api_intent(msg)
            assert intent == "traffic", f"Failed for: {msg}"

    def test_detect_transit_intent(self):
        """Test: 'Bus' / 'Bahn' → transit"""
        # Arrange
        messages = [
            "Wann fährt der nächste Bus?",
            "Nahverkehr Rüsselsheim",
            "Zug nach Frankfurt"
        ]

        # Act & Assert
        for msg in messages:
            intent = api_helper.detect_api_intent(msg)
            assert intent == "transit", f"Failed for: {msg}"

    def test_detect_no_intent(self):
        """Test: General question → None"""
        # Arrange
        messages = [
            "Hallo",
            "Wie geht es dir?",
            "Erzähl mir einen Witz"
        ]

        # Act & Assert
        for msg in messages:
            intent = api_helper.detect_api_intent(msg)
            assert intent is None, f"Should be None for: {msg}"
