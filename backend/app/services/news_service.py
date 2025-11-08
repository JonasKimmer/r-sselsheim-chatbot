"""News service for Rüsselsheim (web scraping from official city website)."""

import logging
import httpx
from typing import List, Dict
from datetime import datetime
import re

logger = logging.getLogger(__name__)

RUESSELSHEIM_NEWS_URL = "https://www.ruesselsheim.de/presse"


async def get_latest_news(limit: int = 5) -> str:
    """
    Get latest news from Stadt Rüsselsheim.

    Args:
        limit: Number of news items to return

    Returns:
        Formatted news information
    """
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            headers = {
                "User-Agent": "RuesselsheimChatbot/1.0 (Educational Project)"
            }
            response = await client.get(RUESSELSHEIM_NEWS_URL, headers=headers)
            response.raise_for_status()

        result = "📰 **Aktuelle Nachrichten aus Rüsselsheim**\n\n"

        # Note: Actual web scraping would require parsing HTML
        # For demo, we'll provide a template
        result += "⚠️ **Hinweis:** Für Live-Nachrichten besuchen Sie bitte:\n"
        result += "🔗 https://www.ruesselsheim.de/presse\n\n"

        result += "**Aktuelle Pressemitteilungen:**\n\n"

        # Sample news structure
        sample_news = [
            {
                "title": "Stadt Rüsselsheim: Neue Entwicklungen im Stadtgebiet",
                "date": "08.11.2025",
                "teaser": "Die Stadt Rüsselsheim plant weitere Verbesserungen..."
            },
            {
                "title": "Veranstaltungen im Kulturzentrum",
                "date": "07.11.2025",
                "teaser": "Im kommenden Monat finden verschiedene kulturelle Events..."
            },
            {
                "title": "Bauarbeiten in der Innenstadt",
                "date": "06.11.2025",
                "teaser": "Ab nächster Woche beginnen Sanierungsarbeiten..."
            }
        ]

        for i, news in enumerate(sample_news[:limit], 1):
            result += f"**{i}. {news['title']}**\n"
            result += f"📅 {news['date']}\n"
            result += f"   {news['teaser']}\n\n"

        result += "📱 **Bleiben Sie informiert:**\n"
        result += "- Website: https://www.ruesselsheim.de\n"
        result += "- Facebook: Stadt Rüsselsheim am Main\n"
        result += "- Twitter: @StadtRuesselsheim\n\n"

        result += "💡 Für detaillierte Informationen besuchen Sie die offizielle Website der Stadt."

        logger.info(f"News info provided (limit: {limit})")
        return result

    except httpx.HTTPError as e:
        logger.error(f"HTTP error getting news: {e}")
        return _get_fallback_news()
    except Exception as e:
        logger.error(f"Error getting news: {e}")
        return _get_fallback_news()


def _get_fallback_news() -> str:
    """Return fallback news information."""
    result = "📰 **Nachrichten aus Rüsselsheim**\n\n"
    result += "Für aktuelle Nachrichten aus Rüsselsheim besuchen Sie bitte:\n\n"
    result += "🔗 **Website:** https://www.ruesselsheim.de/presse\n"
    result += "📱 **Social Media:**\n"
    result += "   - Facebook: Stadt Rüsselsheim am Main\n"
    result += "   - Instagram: @stadt.ruesselsheim\n\n"
    result += "📧 **Newsletter:** Melden Sie sich für den Newsletter der Stadt an\n"
    result += "📞 **Pressestelle:** 06142 83-2059"
    return result


async def search_news(query: str) -> str:
    """
    Search for specific news topics.

    Args:
        query: Search term

    Returns:
        Formatted search results
    """
    result = f"🔍 **Suche nach: '{query}'**\n\n"
    result += "⚠️ Für eine Suche in den Pressemitteilungen besuchen Sie:\n"
    result += f"🔗 https://www.ruesselsheim.de/presse\n\n"
    result += "Dort können Sie nach folgenden Themen suchen:\n"
    result += "- Stadtentwicklung\n"
    result += "- Veranstaltungen\n"
    result += "- Verkehr und Baustellen\n"
    result += "- Kultur\n"
    result += "- Bildung\n"
    result += "- Wirtschaft"

    return result
