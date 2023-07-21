import os

class OpenAI:
    def __init__(self, api_token : str):
        self.api_token = api_token
        os.environ["LLM_API_TOKEN"] = self.api_token
    
    def generate_response(self, data : str) -> str:
        pass