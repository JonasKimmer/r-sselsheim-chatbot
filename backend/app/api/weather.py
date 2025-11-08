"""Weather API endpoints."""

import logging
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from ..services.weather_service import get_weather

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/weather", tags=["weather"])


class CurrentWeather(BaseModel):
    """Current weather data."""
    temperature: Optional[float] = Field(None, description="Temperature in °C")
    feels_like: Optional[float] = Field(None, description="Feels like temperature in °C")
    humidity: Optional[float] = Field(None, description="Humidity in %")
    wind_speed: Optional[float] = Field(None, description="Wind speed in km/h")
    precipitation: Optional[float] = Field(None, description="Precipitation in mm")
    weather_code: Optional[int] = Field(None, description="WMO weather code")
    description: Optional[str] = Field(None, description="Weather description in German")
    time: Optional[str] = Field(None, description="Time of measurement")


class ForecastDay(BaseModel):
    """Daily forecast data."""
    date: str = Field(..., description="Date")
    temp_max: float = Field(..., description="Maximum temperature in °C")
    temp_min: float = Field(..., description="Minimum temperature in °C")
    precipitation: float = Field(..., description="Total precipitation in mm")
    weather_code: int = Field(..., description="WMO weather code")
    description: str = Field(..., description="Weather description in German")


class WeatherResponse(BaseModel):
    """Weather response."""
    city: str = Field(..., description="City name")
    coordinates: Dict[str, float] = Field(..., description="Coordinates")
    current: CurrentWeather = Field(..., description="Current weather")
    forecast: List[ForecastDay] = Field(..., description="3-day forecast")


@router.get("/", response_model=WeatherResponse)
async def get_current_weather(
    city: Optional[str] = Query(None, description="Stadt (Standard: Rüsselsheim am Main)"),
    lat: Optional[float] = Query(None, description="Breitengrad"),
    lon: Optional[float] = Query(None, description="Längengrad")
):
    """
    Wetterdaten abrufen.

    Ruft aktuelle Wetterdaten und 3-Tage-Vorhersage ab.
    Wenn keine Koordinaten angegeben werden, wird Rüsselsheim am Main verwendet.

    **Kostenlos:** Nutzt die Open-Meteo API (keine API-Key erforderlich)

    **Beispiel:**
    - `/api/weather/` - Wetter für Rüsselsheim
    - `/api/weather/?city=Frankfurt&lat=50.1109&lon=8.6821` - Wetter für Frankfurt
    """
    try:
        weather_data = await get_weather(lat=lat, lon=lon, city=city)
        return weather_data
    except Exception as e:
        logger.error(f"Error in weather endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forecast", response_model=Dict[str, Any])
async def get_forecast(
    days: int = Query(3, ge=1, le=7, description="Anzahl der Tage (1-7)"),
    city: Optional[str] = Query(None, description="Stadt (Standard: Rüsselsheim am Main)"),
    lat: Optional[float] = Query(None, description="Breitengrad"),
    lon: Optional[float] = Query(None, description="Längengrad")
):
    """
    Wettervorhersage abrufen.

    Ruft Wettervorhersage für die angegebene Anzahl von Tagen ab (1-7 Tage).

    **Kostenlos:** Nutzt die Open-Meteo API (keine API-Key erforderlich)
    """
    try:
        weather_data = await get_weather(lat=lat, lon=lon, city=city)
        # Return only forecast data
        return {
            "city": weather_data["city"],
            "forecast": weather_data["forecast"][:days]
        }
    except Exception as e:
        logger.error(f"Error in forecast endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
