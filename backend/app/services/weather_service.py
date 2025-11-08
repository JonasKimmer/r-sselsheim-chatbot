"""Weather service using Open-Meteo API (free, no API key required)."""

import logging
import httpx
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Rüsselsheim coordinates
RUESSELSHEIM_LAT = 49.9897
RUESSELSHEIM_LON = 8.4189

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


async def get_weather(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    city: Optional[str] = None
) -> Dict:
    """
    Get weather data from Open-Meteo API.

    Args:
        lat: Latitude (defaults to Rüsselsheim)
        lon: Longitude (defaults to Rüsselsheim)
        city: City name (for display purposes)

    Returns:
        Weather data dictionary
    """
    # Use Rüsselsheim coordinates if not provided
    if lat is None:
        lat = RUESSELSHEIM_LAT
    if lon is None:
        lon = RUESSELSHEIM_LON
    if city is None:
        city = "Rüsselsheim am Main"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
                "hourly": "temperature_2m,precipitation_probability,weather_code",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
                "timezone": "Europe/Berlin",
                "forecast_days": 3
            }

            response = await client.get(OPEN_METEO_URL, params=params)
            response.raise_for_status()

            data = response.json()

            # Parse weather data
            current = data.get("current", {})
            daily = data.get("daily", {})

            weather_code = current.get("weather_code", 0)
            weather_description = _get_weather_description(weather_code)

            result = {
                "city": city,
                "coordinates": {
                    "latitude": lat,
                    "longitude": lon
                },
                "current": {
                    "temperature": current.get("temperature_2m"),
                    "feels_like": current.get("apparent_temperature"),
                    "humidity": current.get("relative_humidity_2m"),
                    "wind_speed": current.get("wind_speed_10m"),
                    "precipitation": current.get("precipitation"),
                    "weather_code": weather_code,
                    "description": weather_description,
                    "time": current.get("time")
                },
                "forecast": []
            }

            # Add 3-day forecast
            if daily and "time" in daily:
                for i in range(min(3, len(daily["time"]))):
                    forecast_day = {
                        "date": daily["time"][i],
                        "temp_max": daily["temperature_2m_max"][i],
                        "temp_min": daily["temperature_2m_min"][i],
                        "precipitation": daily["precipitation_sum"][i],
                        "weather_code": daily["weather_code"][i],
                        "description": _get_weather_description(daily["weather_code"][i])
                    }
                    result["forecast"].append(forecast_day)

            logger.info(f"Successfully fetched weather for {city}")
            return result

    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching weather: {e}")
        raise Exception(f"Fehler beim Abrufen der Wetterdaten: {str(e)}")
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        raise Exception(f"Fehler beim Abrufen der Wetterdaten: {str(e)}")


def _get_weather_description(code: int) -> str:
    """
    Convert WMO weather code to German description.

    WMO Weather interpretation codes (WW):
    https://open-meteo.com/en/docs
    """
    weather_codes = {
        0: "Klar",
        1: "Überwiegend klar",
        2: "Teilweise bewölkt",
        3: "Bewölkt",
        45: "Nebel",
        48: "Gefrierender Nebel",
        51: "Leichter Nieselregen",
        53: "Mäßiger Nieselregen",
        55: "Starker Nieselregen",
        56: "Gefrierender Nieselregen",
        57: "Starker gefrierender Nieselregen",
        61: "Leichter Regen",
        63: "Mäßiger Regen",
        65: "Starker Regen",
        66: "Gefrierender Regen",
        67: "Starker gefrierender Regen",
        71: "Leichter Schneefall",
        73: "Mäßiger Schneefall",
        75: "Starker Schneefall",
        77: "Schneegriesel",
        80: "Leichte Regenschauer",
        81: "Mäßige Regenschauer",
        82: "Starke Regenschauer",
        85: "Leichte Schneeschauer",
        86: "Starke Schneeschauer",
        95: "Gewitter",
        96: "Gewitter mit leichtem Hagel",
        99: "Gewitter mit starkem Hagel"
    }
    return weather_codes.get(code, "Unbekannt")
