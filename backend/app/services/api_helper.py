"""Helper functions to call internal APIs from chat service."""

import logging
from typing import Dict, Any, Optional
from .weather_service import get_weather
from .maps_service import geocode_address, search_nearby
from .traffic_service import get_speed_cameras, get_traffic_info

logger = logging.getLogger(__name__)


async def get_weather_info(city: Optional[str] = None) -> str:
    """
    Get weather information formatted for chat.

    Args:
        city: Optional city name

    Returns:
        Formatted weather information
    """
    try:
        weather_data = await get_weather(city=city)

        current = weather_data["current"]
        forecast = weather_data["forecast"]

        result = f"""🌤️ Aktuelles Wetter in {weather_data['city']}:

**Jetzt:**
- Temperatur: {current['temperature']}°C (gefühlt: {current['feels_like']}°C)
- {current['description']}
- Luftfeuchtigkeit: {current['humidity']}%
- Wind: {current['wind_speed']} km/h
- Niederschlag: {current['precipitation']} mm

**3-Tage-Vorhersage:**"""

        for day in forecast:
            result += f"\n\n**{day['date']}:**"
            result += f"\n- {day['description']}"
            result += f"\n- Min/Max: {day['temp_min']}°C / {day['temp_max']}°C"
            result += f"\n- Niederschlag: {day['precipitation']} mm"

        return result

    except Exception as e:
        logger.error(f"Error getting weather: {e}")
        return "Entschuldigung, ich konnte die Wetterdaten nicht abrufen."


async def find_location(query: str) -> str:
    """
    Find a location by address.

    Args:
        query: Address or location name (or full question)

    Returns:
        Formatted location information
    """
    try:
        # Extract location name from question
        # Remove common question patterns
        search_query = query
        patterns_to_remove = [
            "wo liegt ", "wo ist ", "wo finde ich ",
            "adresse von ", "adresse vom ", "koordinaten von ",
            "das ", "die ", "der ", "?"
        ]

        search_query_lower = query.lower()
        for pattern in patterns_to_remove:
            if pattern in search_query_lower:
                # Find the pattern and remove it
                idx = search_query_lower.find(pattern)
                if idx >= 0:
                    search_query = search_query[idx + len(pattern):]
                    search_query_lower = search_query.lower()

        # Clean up the query
        search_query = search_query.strip().rstrip('?')

        # If still empty or too generic, use original
        if len(search_query) < 3:
            search_query = query

        # Add Rüsselsheim if not already in query
        if "rüsselsheim" not in search_query.lower():
            search_query += " Rüsselsheim"

        results = await geocode_address(search_query, limit=3)

        if not results:
            return f"Ich konnte '{search_query}' nicht finden. Bitte versuchen Sie es mit einem anderen Suchbegriff."

        result = f"📍 Gefundene Orte für '{search_query}':\n"

        for i, location in enumerate(results[:3], 1):
            result += f"\n**{i}. {location['display_name']}**"
            result += f"\n- Koordinaten: {location['latitude']}, {location['longitude']}"

            address = location.get('address', {})
            if 'road' in address:
                result += f"\n- Straße: {address.get('road', '')}"
            if 'house_number' in address:
                result += f" {address.get('house_number', '')}"
            if 'postcode' in address:
                result += f"\n- PLZ: {address.get('postcode', '')}"
            result += "\n"

        return result

    except Exception as e:
        logger.error(f"Error finding location: {e}")
        return "Entschuldigung, ich konnte die Adresse nicht finden."


async def find_nearby_places(query: str, location: str = "Rüsselsheim") -> str:
    """
    Find nearby places.

    Args:
        query: What to search for (restaurant, apotheke, etc.)
        location: Location name (defaults to Rüsselsheim)

    Returns:
        Formatted nearby places
    """
    try:
        # First geocode the location
        locations = await geocode_address(location, limit=1)
        if not locations:
            return f"Ich konnte den Ort '{location}' nicht finden."

        lat = locations[0]['latitude']
        lon = locations[0]['longitude']

        # Search nearby
        places = await search_nearby(lat, lon, query, radius=3000)

        if not places:
            return f"Ich habe keine '{query}' in der Nähe von {location} gefunden."

        result = f"📍 {query.capitalize()} in der Nähe von {location}:\n"

        for i, place in enumerate(places[:5], 1):
            result += f"\n**{i}. {place['display_name']}**"
            result += f"\n- Entfernung: {place['distance_meters']} m"
            result += f"\n- Koordinaten: {place['latitude']}, {place['longitude']}"
            result += "\n"

        return result

    except Exception as e:
        logger.error(f"Error finding nearby places: {e}")
        return "Entschuldigung, ich konnte keine Orte in der Nähe finden."


async def get_speed_camera_info(nearby_location: Optional[str] = None) -> str:
    """
    Get speed camera information.

    Args:
        nearby_location: Optional location to search near

    Returns:
        Formatted speed camera information
    """
    try:
        if nearby_location:
            # Geocode location first
            locations = await geocode_address(nearby_location, limit=1)
            if locations:
                lat = locations[0]['latitude']
                lon = locations[0]['longitude']
                cameras = await get_speed_cameras(lat, lon, radius=5000)
            else:
                cameras = await get_speed_cameras()
        else:
            cameras = await get_speed_cameras()

        if not cameras:
            return "Ich habe keine Blitzer-Informationen gefunden."

        result = "🚦 Bekannte Blitzer in Rüsselsheim:\n"

        for camera in cameras[:6]:
            result += f"\n**{camera['name']}**"
            result += f"\n- Straße: {camera['street']}"
            result += f"\n- Typ: {'Festinstalliert' if camera['type'] == 'fixed' else 'Häufige mobile Kontrolle'}"
            result += f"\n- Tempolimit: {camera['speed_limit']} km/h"
            result += f"\n- Richtung: {camera['direction']}"
            if camera.get('distance_meters'):
                result += f"\n- Entfernung: {camera['distance_meters']} m"
            result += "\n"

        result += "\n⚠️ **Hinweis:** Mobile Blitzer können auch an anderen Stellen aufgestellt werden. Bitte beachten Sie immer die Verkehrsregeln!"

        return result

    except Exception as e:
        logger.error(f"Error getting speed cameras: {e}")
        return "Entschuldigung, ich konnte keine Blitzer-Informationen abrufen."


def detect_api_intent(message: str) -> Optional[str]:
    """
    Detect if message requires API call.

    Args:
        message: User message

    Returns:
        API intent or None
    """
    message_lower = message.lower()

    # Weather keywords
    if any(word in message_lower for word in ["wetter", "temperatur", "regen", "schnee", "vorhersage", "wettervorhersage", "grad", "warm", "kalt"]):
        return "weather"

    # Specific location search (e.g., "Wo liegt Restaurant X", "Adresse von Y")
    # Check this BEFORE nearby search to prioritize specific location queries
    if any(phrase in message_lower for phrase in ["wo liegt", "wo ist", "adresse von", "adresse vom", "wo finde ich", "koordinaten von"]):
        return "location"

    # Nearby search keywords (e.g., "Restaurants in der Nähe")
    if any(word in message_lower for word in ["in der nähe", "nähe", "nahegelegene", "nahe"]):
        return "nearby"

    # Traffic keywords
    if any(word in message_lower for word in ["blitzer", "radarfalle", "geschwindigkeitskontrolle", "tempolimit"]):
        return "traffic"

    return None
