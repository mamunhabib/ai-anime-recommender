import os
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

class VectorStoreManager:
    def __init__(self, data_path: str, persist_directory: str):
        self.data_path = data_path
        self.persist_directory = persist_directory
        # This triggers the automatic Hugging Face download we talked about!
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    def create_vector_store(self):
        try:
            logger.info("Starting Vector Store Creation...")
            # 1. Load the preprocessed CSV
            loader = CSVLoader(file_path=self.data_path, encoding='utf-8')
            data = loader.load()
            
            # 2. Embed the text and save to ChromaDB
            vector_store = Chroma.from_documents(
                documents=data,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            logger.info("Vector Store Created Successfully.")
            return vector_store
        
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise CustomException(e, e)
            
    def load_vector_store(self):
        # 3. Load an existing database so we don't have to embed it again
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
