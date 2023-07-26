import os
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

class OpenAI:
    def __init__(self, api_token : str):
        self.api_token = api_token
        os.environ["OPEN_AI_KEY"] = self.api_token
    
    def predict(self, query : str, vector_store_index_creator : VectorstoreIndexCreator):
        return vector_store_index_creator.query(query, llm=ChatOpenAI)