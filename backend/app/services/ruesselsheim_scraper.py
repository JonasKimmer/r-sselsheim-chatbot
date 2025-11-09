"""Web scraper for ruesselsheim.de official website."""

import logging
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from .rag_service import RAGService
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class RuesselsheimScraper:
    """Scraper for importing content from ruesselsheim.de"""

    # Important pages to scrape
    IMPORTANT_PAGES = [
        "https://www.ruesselsheim.de/leben-wohnen/buergerservice/",
        "https://www.ruesselsheim.de/leben-wohnen/buergerservice/personalausweis/",
        "https://www.ruesselsheim.de/leben-wohnen/buergerservice/reisepass/",
        "https://www.ruesselsheim.de/rathaus/",
        "https://www.ruesselsheim.de/rathaus/oeffnungszeiten/",
        "https://www.ruesselsheim.de/leben-wohnen/bildung/",
        "https://www.ruesselsheim.de/leben-wohnen/kultur/",
        "https://www.ruesselsheim.de/wirtschaft/",
    ]

    def __init__(self, db: Session):
        """Initialize scraper."""
        self.db = db
        self.rag_service = RAGService(db)

    async def scrape_page(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrape content from a single page.

        Args:
            url: URL to scrape

        Returns:
            Dictionary with title, content, and url
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()

                # Extract title
                title = ""
                if soup.find('h1'):
                    title = soup.find('h1').get_text(strip=True)
                elif soup.find('title'):
                    title = soup.find('title').get_text(strip=True)

                # Extract main content
                content = ""
                main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')

                if main_content:
                    # Get text and clean it
                    content = main_content.get_text(separator='\n', strip=True)
                    # Remove excessive whitespace
                    content = '\n'.join(line.strip() for line in content.split('\n') if line.strip())

                if not content:
                    logger.warning(f"No content found on {url}")
                    return None

                logger.info(f"Successfully scraped {url}: {len(content)} chars")

                return {
                    "title": title,
                    "content": content,
                    "url": url
                }

        except httpx.HTTPError as e:
            logger.error(f"HTTP error scraping {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None

    async def import_page_to_rag(self, url: str, category: str = "verwaltung") -> bool:
        """
        Scrape a page and import it to RAG system.

        Args:
            url: URL to scrape
            category: Document category

        Returns:
            True if successful, False otherwise
        """
        page_data = await self.scrape_page(url)

        if not page_data:
            return False

        try:
            # Add to RAG database
            self.rag_service.add_document(
                title=page_data["title"],
                content=page_data["content"],
                category=category,
                source=page_data["url"]
            )

            logger.info(f"Imported to RAG: {page_data['title']}")
            return True

        except Exception as e:
            logger.error(f"Error importing to RAG: {e}")
            return False

    async def import_all_important_pages(self) -> Dict[str, int]:
        """
        Import all important pages from ruesselsheim.de

        Returns:
            Dictionary with success/failure counts
        """
        results = {
            "success": 0,
            "failed": 0,
            "total": len(self.IMPORTANT_PAGES)
        }

        for url in self.IMPORTANT_PAGES:
            logger.info(f"Importing {url}...")

            success = await self.import_page_to_rag(url)

            if success:
                results["success"] += 1
            else:
                results["failed"] += 1

        logger.info(f"Import complete: {results['success']}/{results['total']} successful")
        return results

    async def scrape_sitemap(self) -> List[str]:
        """
        Scrape sitemap to find all available URLs.

        Returns:
            List of URLs from sitemap
        """
        sitemap_url = "https://www.ruesselsheim.de/sitemap.xml"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(sitemap_url)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'xml')
                urls = [loc.text for loc in soup.find_all('loc')]

                logger.info(f"Found {len(urls)} URLs in sitemap")
                return urls

        except Exception as e:
            logger.error(f"Error scraping sitemap: {e}")
            return []
