from langchain_core.prompts import PromptTemplate

def get_prompt_template():
    prompt_template = """
    You are an Anime Recommendation Expert. 
    Use the following pieces of retrieved context (anime details) to recommend an anime to the user based on their question.
    If you don't know the answer or the retrieved context doesn't match the question, just say you don't have a good recommendation. 
    Don't make up an anime that isn't in the context!
    
    Context: {context}
    
    Question: {input}
    
    Recommendation and Explanation:
    """
    
    # Notice we changed "question" to "input" here too!
    prompt = PromptTemplate(
        template=prompt_template, 
        input_variables=["context", "input"]
    )
    return prompt
