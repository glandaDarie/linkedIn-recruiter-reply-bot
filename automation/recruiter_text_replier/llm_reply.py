from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from utils.file_utils import read_content
from utils.paths_utils import llm_api_token_path
import os

class LLM_Reply_controller:
    def __init__(self):
        credentials : str = read_content(llm_api_token_path)
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = credentials["api_token"]
        
    @staticmethod
    def prediction_hugging_face(data : str, template : str, repo_id : str = "google/flan-t5-xxl", **kwargs : dict) -> str:
        prompt : PromptTemplate = PromptTemplate(template=template, input_variables=["data"])
        llm : HuggingFaceHub = HuggingFaceHub(
            repo_id=repo_id, model_kwargs=kwargs
        )
        llm_chain : LLMChain = LLMChain(prompt=prompt, llm=llm)
        return llm_chain.run(data)
    
    @staticmethod
    def prediction_openAI(data : str) -> str:
        pass