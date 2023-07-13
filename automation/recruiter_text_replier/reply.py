from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
from utils.file_utils import read_credentials
from utils.paths_utils import hugging_face_api_token_path
import os

class Reply_controller:
    def __init__(self):
        credentials : str = read_credentials(hugging_face_api_token_path)
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = credentials["api_token"]

    @staticmethod
    def prediction(data : str, template : str, **kwargs : dict) -> str:
        prompt : PromptTemplate = PromptTemplate(template=template, input_variables=["data"])
        repo_id : str = "google/flan-t5-xxl"
        llm : HuggingFaceHub = HuggingFaceHub(
            repo_id=repo_id, model_kwargs={"temperature": 0.2, "max_length": 200}
        )
        llm_chain : LLMChain = LLMChain(prompt=prompt, llm=llm)
        return llm_chain.run(data)
    