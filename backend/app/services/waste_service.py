"""Waste calendar service for Rüsselsheim."""

import logging
from typing import Dict, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


# Sample waste collection schedule (would be loaded from city API or database)
def get_next_collection_dates():
    """Generate next collection dates (demo data)."""
    today = datetime.now()

    # Calculate next collection days (example: every Monday for Restmüll, etc.)
    next_monday = today + timedelta(days=(7 - today.weekday()) % 7)
    next_tuesday = today + timedelta(days=(8 - today.weekday()) % 7)
    next_wednesday = today + timedelta(days=(9 - today.weekday()) % 7)
    next_thursday = today + timedelta(days=(10 - today.weekday()) % 7)

    return {
        "restmuell": next_monday.strftime("%d.%m.%Y"),
        "biomuell": next_tuesday.strftime("%d.%m.%Y"),
        "papier": next_wednesday.strftime("%d.%m.%Y"),
        "gelber_sack": next_thursday.strftime("%d.%m.%Y")
    }


async def get_waste_calendar(street: str = None, house_number: str = None) -> str:
    """
    Get waste collection calendar for Rüsselsheim.

    Args:
        street: Street name (optional)
        house_number: House number (optional)

    Returns:
        Formatted waste collection schedule
    """
    try:
        dates = get_next_collection_dates()

        result = "♻️ **Abfallkalender Rüsselsheim am Main**\n\n"

        if street:
            result += f"📍 Adresse: {street}"
            if house_number:
                result += f" {house_number}"
            result += "\n\n"

        result += "**Nächste Abholtermine:**\n\n"
        result += f"🗑️ **Restmüll (schwarze Tonne):** {dates['restmuell']}\n"
        result += f"🍃 **Bioabfall (braune Tonne):** {dates['biomuell']}\n"
        result += f"📄 **Papier (blaue Tonne):** {dates['papier']}\n"
        result += f"💛 **Gelber Sack:** {dates['gelber_sack']}\n\n"

        result += "⚠️ **Hinweis:** Dies sind beispielhafte Termine.\n"
        result += "Für Ihre genauen Abholtermine besuchen Sie:\n"
        result += "🔗 https://www.ruesselsheim.de/abfallkalender\n\n"

        result += "**Wertstoffhof Rüsselsheim:**\n"
        result += "📍 Borsigstraße 3, 65428 Rüsselsheim\n"
        result += "🕒 Mo-Fr: 8:00-17:00 Uhr, Sa: 8:00-13:00 Uhr\n"
        result += "📞 Abfallberatung: 06142 83-2710"

        logger.info("Waste calendar info provided")
        return result

    except Exception as e:
        logger.error(f"Error getting waste calendar: {e}")
        return "Entschuldigung, ich konnte den Abfallkalender nicht abrufen."


async def get_waste_info(waste_type: str) -> str:
    """
    Get information about specific waste type.

    Args:
        waste_type: Type of waste (restmüll, bioabfall, papier, etc.)

    Returns:
        Information about waste disposal
    """
    waste_info = {
        "restmüll": {
            "name": "Restmüll (schwarze Tonne)",
            "description": "Nicht verwertbarer Abfall, der nicht in andere Tonnen gehört",
            "examples": "Staubsaugerbeutel, Windeln, Hygieneartikel, kaputtes Spielzeug",
            "not_allowed": "Elektrogeräte, Batterien, Sondermüll, Wertstoffe"
        },
        "biomüll": {
            "name": "Bioabfall (braune Tonne)",
            "description": "Organische Abfälle aus Küche und Garten",
            "examples": "Obst- und Gemüsereste, Kaffeesatz, Gartenabfälle, Laub",
            "not_allowed": "Plastiktüten, gekochte Essensreste mit Fleisch, Katzenstreu"
        },
        "papier": {
            "name": "Papier und Karton (blaue Tonne)",
            "description": "Altpapier und Kartonagen",
            "examples": "Zeitungen, Zeitschriften, Kartons, Papierverpackungen",
            "not_allowed": "Beschichtetes Papier, Tapeten, verschmutztes Papier"
        },
        "gelber_sack": {
            "name": "Gelber Sack / Gelbe Tonne",
            "description": "Verpackungen aus Kunststoff, Metall und Verbundstoffen",
            "examples": "Joghurtbecher, Konservendosen, Folien, Tetrapaks",
            "not_allowed": "Restmüll, Glas, Elektrogeräte"
        }
    }

    waste_type_lower = waste_type.lower()
    info = waste_info.get(waste_type_lower)

    if not info:
        # Try partial match
        for key, value in waste_info.items():
            if waste_type_lower in key or key in waste_type_lower:
                info = value
                break

    if info:
        result = f"♻️ **{info['name']}**\n\n"
        result += f"**Beschreibung:** {info['description']}\n\n"
        result += f"**Beispiele:** {info['examples']}\n\n"
        result += f"❌ **Nicht erlaubt:** {info['not_allowed']}"
        return result
    else:
        return "Ich konnte keine Informationen zu dieser Abfallart finden. Bitte versuchen Sie: Restmüll, Biomüll, Papier oder Gelber Sack."
