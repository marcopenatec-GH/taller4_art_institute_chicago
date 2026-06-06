import logging
import os
from dataclasses import dataclass
from typing import Any

import requests
from dotenv import load_dotenv
from pymongo import ASCENDING, MongoClient
from pymongo.collection import Collection


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Settings:
    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    mongo_db: str = os.getenv("MONGO_DB", "taller4_db")
    mongo_collection: str = os.getenv("MONGO_COLLECTION", "raw_data")
    api_url: str = os.getenv("API_URL", "https://api.artic.edu/api/v1/artworks")
    target_records: int = int(os.getenv("TARGET_RECORDS", "100"))
    page_size: int = int(os.getenv("PAGE_SIZE", "100"))


def get_raw_collection(settings: Settings) -> Collection:
    """Connect to MongoDB and return the target RAW collection."""
    client = MongoClient(settings.mongo_uri)
    collection = client[settings.mongo_db][settings.mongo_collection]
    collection.create_index([("id", ASCENDING)], unique=True)
    return collection


def fetch_artworks(api_url: str, page: int, limit: int) -> list[dict[str, Any]]:
    """Download one page of raw artwork objects from the API."""
    params = {"page": page, "limit": limit}
    response = requests.get(api_url, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload.get("data", [])


def save_raw_artworks(collection: Collection, artworks: list[dict[str, Any]]) -> int:
    """Store raw API documents using the API id as natural key."""
    processed = 0

    for artwork in artworks:
        artwork_id = artwork.get("id")

        if artwork_id is None:
            logger.warning("Skipping document without API id")
            continue

        collection.replace_one({"id": artwork_id}, artwork, upsert=True)
        processed += 1

    return processed


def validate_raw_load(collection: Collection, minimum_records: int) -> None:
    """Run basic post-load checks required by the workshop."""
    total_documents = collection.count_documents({})
    unique_ids = len(collection.distinct("id"))
    sample_document = collection.find_one({}, {"_id": 0})
    sample_fields = sorted(sample_document.keys())[:12] if sample_document else []

    logger.info("Post-load validation")
    logger.info("Documents in collection: %s", total_documents)
    logger.info("Unique API ids: %s", unique_ids)
    logger.info("Sample RAW fields: %s", sample_fields)

    if total_documents < minimum_records:
        raise ValueError(
            f"Expected at least {minimum_records} documents, but found {total_documents}."
        )


def main() -> None:
    """EXTRACT and RAW LOAD: fetch API records and store them in MongoDB."""
    settings = Settings()
    collection = get_raw_collection(settings)

    processed_records = 0
    page = 1

    logger.info("Starting API extract from Art Institute of Chicago")
    logger.info("Source endpoint: %s", settings.api_url)
    logger.info("Target MongoDB: %s.%s", settings.mongo_db, settings.mongo_collection)
    logger.info("Target record count: %s", settings.target_records)

    while processed_records < settings.target_records:
        remaining = settings.target_records - processed_records
        limit = min(settings.page_size, remaining)
        artworks = fetch_artworks(settings.api_url, page=page, limit=limit)

        if not artworks:
            logger.warning("The API did not return more records.")
            break

        saved_in_page = save_raw_artworks(collection, artworks)
        processed_records += saved_in_page
        logger.info("Page %s processed. Records processed: %s", page, processed_records)
        page += 1

    validate_raw_load(collection, settings.target_records)
    logger.info("Pipeline finished successfully.")


if __name__ == "__main__":
    main()
