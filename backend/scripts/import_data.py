"""Import initial data into the database."""

import sys
import json
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db import SessionLocal, init_db
from app.services import RAGService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def import_documents(data_file: str = "../data/ruesselsheim_data.json"):
    """Import documents from JSON file.

    Args:
        data_file: Path to JSON data file
    """
    logger.info("Initializing database...")
    init_db()

    logger.info(f"Loading data from {data_file}...")
    data_path = Path(__file__).parent / data_file

    with open(data_path, 'r', encoding='utf-8') as f:
        documents = json.load(f)

    logger.info(f"Found {len(documents)} documents to import")

    db = SessionLocal()
    try:
        rag_service = RAGService(db)

        for idx, doc in enumerate(documents, 1):
            logger.info(f"Importing document {idx}/{len(documents)}: {doc['title']}")

            rag_service.add_document(
                title=doc['title'],
                content=doc['content'],
                category=doc['category'],
                source=doc.get('source'),
                doc_metadata=doc.get('metadata')
            )

        logger.info("All documents imported successfully!")

    except Exception as e:
        logger.error(f"Error importing documents: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import_documents()
