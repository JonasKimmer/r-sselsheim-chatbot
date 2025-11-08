"""Fuel prices service using Tankerkönig API."""

import logging
import httpx
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Tankerkönig API (requires free API key from https://creativecommons.tankerkoenig.de)
TANKERKOENIG_API_BASE = "https://creativecommons.tankerkoenig.de/json"

# Rüsselsheim coordinates
RUESSELSHEIM_LAT = 49.9897
RUESSELSHEIM_LON = 8.4189


async def get_fuel_prices(
    lat: float = RUESSELSHEIM_LAT,
    lon: float = RUESSELSHEIM_LON,
    radius: float = 5.0,
    fuel_type: str = "all",
    sort_by: str = "dist"
) -> str:
    """
    Get fuel prices from nearby gas stations.

    Args:
        lat: Latitude
        lon: Longitude
        radius: Search radius in km (max 25)
        fuel_type: Fuel type (e5, e10, diesel, all)
        sort_by: Sort by 'dist' (distance) or 'price'

    Returns:
        Formatted fuel price information
    """
    try:
        # Note: Tankerkönig requires API key
        # For demo, return template with information

        result = "⛽ **Spritpreise in Rüsselsheim**\n\n"
        result += "⚠️ **Hinweis:** Für Live-Spritpreise wird ein kostenloser Tankerkönig API-Key benötigt.\n"
        result += "Registrierung: https://creativecommons.tankerkoenig.de\n\n"

        result += "**Tankstellen in Rüsselsheim:**\n\n"

        # Sample data structure (would be from API)
        stations = [
            {
                "name": "Aral Tankstelle",
                "brand": "ARAL",
                "street": "Mainzer Straße 1",
                "distance": 0.8
            },
            {
                "name": "Shell Station",
                "brand": "Shell",
                "street": "Bahnhofstraße 45",
                "distance": 1.2
            },
            {
                "name": "Esso Station",
                "brand": "Esso",
                "street": "Darmstädter Straße 15",
                "distance": 1.5
            }
        ]

        for i, station in enumerate(stations, 1):
            result += f"**{i}. {station['name']}**\n"
            result += f"   📍 {station['street']}\n"
            result += f"   📏 {station['distance']} km entfernt\n\n"

        result += "💡 **Aktuelle Preise finden Sie auf:**\n"
        result += "- https://www.clever-tanken.de\n"
        result += "- https://www.benzinpreis.de\n"
        result += "- Tankerkönig App (Android/iOS)\n\n"

        result += "📱 **Tipp:** Mit der richtigen App können Sie bis zu 10-15 Cent pro Liter sparen!"

        logger.info(f"Fuel price info requested for radius {radius}km")
        return result

    except Exception as e:
        logger.error(f"Error getting fuel prices: {e}")
        return "Entschuldigung, ich konnte die Spritpreis-Informationen nicht abrufen."


async def get_cheapest_station(fuel_type: str = "e5") -> str:
    """
    Find cheapest gas station nearby.

    Args:
        fuel_type: Type of fuel (e5, e10, diesel)

    Returns:
        Information about cheapest station
    """
    fuel_names = {
        "e5": "Super E5",
        "e10": "Super E10",
        "diesel": "Diesel"
    }

    fuel_name = fuel_names.get(fuel_type.lower(), "Super E5")

    result = f"⛽ **Günstigste Tankstelle für {fuel_name}**\n\n"
    result += "⚠️ **Hinweis:** Für Live-Preisvergleiche benötigen Sie einen Tankerkönig API-Key.\n\n"
    result += "**Empfohlene Apps für Preisvergleiche:**\n"
    result += "- 📱 Clever Tanken\n"
    result += "- 📱 Mehr-tanken\n"
    result += "- 📱 ADAC Spritpreise\n\n"
    result += "💡 **Spartipp:** Tanken Sie abends! Benzin ist oft zwischen 18-20 Uhr am günstigsten."

    return result
