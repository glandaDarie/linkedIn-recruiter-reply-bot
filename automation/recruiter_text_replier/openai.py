from typing import Dict
import os
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import ConversationalRetrievalChain
from utils.paths_utils import personal_data_path

class OpenAI:
    def __init__(self, api_token : str):
        self.api_token = api_token
        os.environ["OPENAI_API_KEY"] = self.api_token
    
    def predict(self, query : str, model : str = "gpt-3.5-turbo") -> str:
        personal_data_loader : TextLoader = TextLoader(personal_data_path)
        index : VectorstoreIndexCreator = VectorstoreIndexCreator().from_loaders([personal_data_loader])
        chain : ConversationalRetrievalChain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model=model),
            retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
        )
        result : Dict[str, str] = chain({"question": query, "chat_history": []})
        return result["answer"]