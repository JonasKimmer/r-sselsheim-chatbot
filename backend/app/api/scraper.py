"""Web scraping API endpoints for ruesselsheim.de"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
from ..db import get_db
from ..services.ruesselsheim_scraper import RuesselsheimScraper

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/scraper", tags=["scraper"])


@router.post("/import/important-pages")
async def import_important_pages(
    db: Session = Depends(get_db)
) -> Dict[str, int]:
    """
    Import all important pages from ruesselsheim.de to RAG system.

    This will scrape predefined important pages and add them to the
    document database for semantic search.

    Returns:
        Statistics about the import (success, failed, total)
    """
    try:
        scraper = RuesselsheimScraper(db)
        results = await scraper.import_all_important_pages()

        logger.info(f"Import completed: {results}")
        return results

    except Exception as e:
        logger.error(f"Error during import: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import/page")
async def import_single_page(
    url: str,
    category: str = "verwaltung",
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Import a single page from ruesselsheim.de

    Args:
        url: URL to scrape and import
        category: Document category (default: verwaltung)

    Returns:
        Status message
    """
    try:
        scraper = RuesselsheimScraper(db)
        success = await scraper.import_page_to_rag(url, category)

        if success:
            return {
                "status": "success",
                "message": f"Successfully imported {url}"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to import {url}"
            )

    except Exception as e:
        logger.error(f"Error importing page: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sitemap")
async def get_sitemap_urls(
    db: Session = Depends(get_db)
) -> List[str]:
    """
    Get all URLs from ruesselsheim.de sitemap.

    Returns:
        List of URLs available on the website
    """
    try:
        scraper = RuesselsheimScraper(db)
        urls = await scraper.scrape_sitemap()

        return urls

    except Exception as e:
        logger.error(f"Error getting sitemap: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/preview")
async def preview_page(
    url: str,
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Preview what content would be extracted from a URL.

    Args:
        url: URL to preview

    Returns:
        Extracted title and content (first 500 chars)
    """
    try:
        scraper = RuesselsheimScraper(db)
        page_data = await scraper.scrape_page(url)

        if not page_data:
            raise HTTPException(
                status_code=404,
                detail=f"Could not scrape {url}"
            )

        return {
            "title": page_data["title"],
            "content_preview": page_data["content"][:500] + "...",
            "content_length": len(page_data["content"]),
            "url": page_data["url"]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error previewing page: {e}")
        raise HTTPException(status_code=500, detail=str(e))
