from typing import List, Dict
from pymongo import MongoClient
from utils.paths_utils import database_credentials_path
from utils.file_utils import read_credentials

class Chat_dao:
    def __init__(self, data : List[List[str]]):
        db_credentials : dict = read_credentials(database_credentials_path)
        cluster : MongoClient = MongoClient(f"mongodb+srv://{db_credentials['username']}:{db_credentials['password']}@linkedin-bot.iac0yve.mongodb.net/?retryWrites=true&w=majority")
        mongo = cluster[db_credentials['db_name']]
        self.collection = mongo[db_credentials['db_name']]
        self.data : Dict[str, str] = {str(index) : " - ".join(name_text) for index, name_text in enumerate(data)}

    def insert(self) -> None|Exception:
        try:
            self.collection.insert_one(self.data)
        except Exception as e:
            return e
        return None
    
    def update(self):
        pass

    def delete(self):
        pass