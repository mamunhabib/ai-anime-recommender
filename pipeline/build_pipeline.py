import os
from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreManager
from utils.logger import get_logger

logger = get_logger(__name__)

def build():
    # 1. Define where our files live
    original_csv = "data/anime_with_synopsis.csv"
    processed_csv = "data/processed_anime.csv"
    persist_directory = "chroma_db"

    # 2. Trigger the Data Loader
    logger.info("Step 1: Starting Data Loading and Processing...")
    data_loader = AnimeDataLoader(original_csv, processed_csv)
    data_loader.load_and_process()
    logger.info("Step 1 Complete: Data Processed.")

    # 3. Trigger the Vector Store Creation
    logger.info("Step 2: Starting Vector Database Creation (This may take a few minutes)...")
    vector_manager = VectorStoreManager(processed_csv, persist_directory)
    vector_manager.create_vector_store()
    logger.info("Step 2 Complete: Vector Database Built successfully!")

if __name__ == "__main__":
    build()
