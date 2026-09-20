import os
from src.vector_store import VectorStoreManager
from src.recommender import AnimeRecommender
from utils.logger import get_logger

logger = get_logger(__name__)

def get_anime_recommendation(query: str) -> str:
    # 1. Define where the database lives
    persist_directory = "chroma_db"
    
    logger.info("Initializing the Recommendation Pipeline...")
    
    # 2. LOAD the database (Notice we use load_vector_store, NOT create)
    vector_manager = VectorStoreManager(data_path="", persist_directory=persist_directory)
    vector_store = vector_manager.load_vector_store()
    
    # 3. Fire up the Recommender Engine
    recommender = AnimeRecommender(vector_store)
    
    # 4. Get the answer!
    result = recommender.get_recommendation(query)
    return result

# You can actually test this file directly if you run it!
if __name__ == "__main__":
    test_query = "I want a really sad anime about time travel."
    print("\n[User]:", test_query)
    print("\n[AI]:", get_anime_recommendation(test_query))
