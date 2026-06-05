import os
from typing import Any

import requests
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "taller4_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "raw_data")

API_URL = os.getenv("API_URL", "https://api.artic.edu/api/v1/artworks")
TARGET_RECORDS = int(os.getenv("TARGET_RECORDS", "100"))
PAGE_SIZE = int(os.getenv("PAGE_SIZE", "100"))


def fetch_artworks(page: int, limit: int) -> list[dict[str, Any]]:
    """Download one page of raw artwork objects from the API."""
    response = requests.get(API_URL, params={"page": page, "limit": limit}, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload.get("data", [])


def main() -> None:
    """Fetch raw API records and store them in MongoDB."""
    client = MongoClient(MONGO_URI)
    collection = client[MONGO_DB][MONGO_COLLECTION]

    collection.create_index("id", unique=True)

    total_saved = 0
    page = 1

    print("Iniciando ingesta desde Art Institute of Chicago API")
    print(f"Base de datos MongoDB: {MONGO_DB}")
    print(f"Coleccion MongoDB: {MONGO_COLLECTION}")

    while total_saved < TARGET_RECORDS:
        artworks = fetch_artworks(page=page, limit=PAGE_SIZE)

        if not artworks:
            print("La API no devolvio mas registros.")
            break

        for artwork in artworks:
            artwork_id = artwork.get("id")

            if artwork_id is None:
                continue

            collection.replace_one({"id": artwork_id}, artwork, upsert=True)
            total_saved += 1

            if total_saved >= TARGET_RECORDS:
                break

        print(f"Pagina {page} procesada. Registros guardados en esta ejecucion: {total_saved}")
        page += 1

    total_documents = collection.count_documents({})
    print("Ingesta finalizada.")
    print(f"Documentos actuales en {MONGO_DB}.{MONGO_COLLECTION}: {total_documents}")


if __name__ == "__main__":
    main()
