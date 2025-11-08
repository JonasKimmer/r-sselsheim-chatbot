"""German holidays service using feiertage-api.de (free, no API key required)."""

import logging
import httpx
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

FEIERTAGE_API_URL = "https://feiertage-api.de/api/"


async def get_holidays(year: int = None, state: str = "HE") -> str:
    """
    Get German holidays for Hessen.

    Args:
        year: Year (default: current year)
        state: State code (HE = Hessen)

    Returns:
        Formatted holidays information
    """
    try:
        if year is None:
            year = datetime.now().year

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{FEIERTAGE_API_URL}?jahr={year}&nur_land={state}")
            response.raise_for_status()

            holidays = response.json()

        result = f"📅 **Feiertage in Hessen {year}**\n\n"

        # Sort holidays by date
        sorted_holidays = sorted(
            holidays.items(),
            key=lambda x: datetime.fromisoformat(x[1]['datum'])
        )

        for name, info in sorted_holidays:
            date = datetime.fromisoformat(info['datum'])
            date_str = date.strftime("%d.%m.%Y (%A)")

            result += f"**{name}**\n"
            result += f"📅 {date_str}\n"

            if info.get('hinweis'):
                result += f"ℹ️ {info['hinweis']}\n"

            result += "\n"

        logger.info(f"Holidays info provided for year {year}")
        return result

    except httpx.HTTPError as e:
        logger.error(f"HTTP error getting holidays: {e}")
        return "Entschuldigung, ich konnte die Feiertagsinformationen nicht abrufen."
    except Exception as e:
        logger.error(f"Error getting holidays: {e}")
        return "Entschuldigung, ich konnte die Feiertagsinformationen nicht abrufen."


async def is_holiday_today() -> str:
    """
    Check if today is a holiday in Hessen.

    Returns:
        Information about today's holiday status
    """
    try:
        today = datetime.now()
        year = today.year

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{FEIERTAGE_API_URL}?jahr={year}&nur_land=HE")
            response.raise_for_status()

            holidays = response.json()

        today_str = today.strftime("%Y-%m-%d")

        for name, info in holidays.items():
            if info['datum'] == today_str:
                result = f"✅ **Ja, heute ist ein Feiertag!**\n\n"
                result += f"🎉 **{name}**\n"
                result += f"📅 {today.strftime('%d.%m.%Y')}\n"

                if info.get('hinweis'):
                    result += f"\nℹ️ {info['hinweis']}"

                return result

        result = f"❌ **Nein, heute ist kein Feiertag.**\n\n"
        result += f"📅 {today.strftime('%d.%m.%Y (%A)')}\n\n"

        # Find next holiday
        for name, info in sorted(holidays.items(), key=lambda x: datetime.fromisoformat(x[1]['datum'])):
            holiday_date = datetime.fromisoformat(info['datum'])
            if holiday_date > today:
                days_until = (holiday_date - today).days
                result += f"**Nächster Feiertag:**\n"
                result += f"🎉 {name}\n"
                result += f"📅 {holiday_date.strftime('%d.%m.%Y')} (in {days_until} Tagen)"
                break

        return result

    except Exception as e:
        logger.error(f"Error checking holiday: {e}")
        return "Entschuldigung, ich konnte die Feiertagsinformationen nicht abrufen."


async def get_next_holiday() -> str:
    """
    Get information about the next upcoming holiday.

    Returns:
        Information about next holiday
    """
    try:
        today = datetime.now()
        year = today.year

        async with httpx.AsyncClient(timeout=10.0) as client:
            # Check current and next year
            response_current = await client.get(f"{FEIERTAGE_API_URL}?jahr={year}&nur_land=HE")
            response_next = await client.get(f"{FEIERTAGE_API_URL}?jahr={year+1}&nur_land=HE")

            response_current.raise_for_status()
            response_next.raise_for_status()

            all_holidays = {**response_current.json(), **response_next.json()}

        # Find next holiday
        for name, info in sorted(all_holidays.items(), key=lambda x: datetime.fromisoformat(x[1]['datum'])):
            holiday_date = datetime.fromisoformat(info['datum'])
            if holiday_date >= today:
                days_until = (holiday_date - today).days

                result = f"🎉 **Nächster Feiertag:**\n\n"
                result += f"**{name}**\n"
                result += f"📅 {holiday_date.strftime('%d.%m.%Y (%A)')}\n"

                if days_until == 0:
                    result += "⏰ **Heute!**\n"
                elif days_until == 1:
                    result += "⏰ **Morgen!**\n"
                else:
                    result += f"⏰ In **{days_until} Tagen**\n"

                if info.get('hinweis'):
                    result += f"\nℹ️ {info['hinweis']}"

                return result

        return "Keine weiteren Feiertage gefunden."

    except Exception as e:
        logger.error(f"Error getting next holiday: {e}")
        return "Entschuldigung, ich konnte die Feiertagsinformationen nicht abrufen."
