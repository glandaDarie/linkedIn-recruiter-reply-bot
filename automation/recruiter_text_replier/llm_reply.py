from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from utils.file_utils import read_content
from utils.paths_utils import llm_api_token_path
import os

class LLM_Reply_controller:
    def __init__(self, api_token : str):
        self.api_token = api_token
        os.environ["LLM_API_TOKEN"] = self.api_token
        
    def prediction_hugging_face(self, data : str, template : str, repo_id : str = "google/flan-t5-xxl", **kwargs : dict) -> str:
        prompt : PromptTemplate = PromptTemplate(template=template, input_variables=["data"])
        llm : HuggingFaceHub = HuggingFaceHub(
            repo_id=repo_id, model_kwargs=kwargs
        )
        llm_chain : LLMChain = LLMChain(prompt=prompt, llm=llm)
        return llm_chain.run(data)
    
    def prediction_openAI(self, data : str) -> str:
        pass