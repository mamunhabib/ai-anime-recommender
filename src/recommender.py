import os
from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from src.prompt_template import get_prompt_template
from config.config import GROQ_API_KEY, MODEL_NAME
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

class AnimeRecommender:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        # 1. Initialize the ultra-fast Llama-3 model using Groq
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=MODEL_NAME,
            temperature=0.5 # 0.5 allows for some creativity, but stays mostly factual
        )
        self.prompt = get_prompt_template()

    def get_recommendation(self, user_query: str) -> str:
        try:
            logger.info(f"Generating recommendation for query: '{user_query}'")
            
            # 2. Turn the ChromaDB into a "Retriever" (a search engine)
            # We tell it to return the top 5 closest anime matches
            retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
            
            # 3. Create the Question-Answering Chain
            # This combines the LLM and the Prompt Template
            question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
            
            # 4. Create the Final RAG Chain
            # This connects the Search Engine to the Question-Answering Chain
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)
            
            # 5. Run the Chain!
            response = rag_chain.invoke({"input": user_query})
            
            logger.info("Recommendation generated successfully.")
            return response["answer"]
            
        except Exception as e:
            logger.error(f"Error in generating recommendation: {e}")
            raise CustomException(e, e)
