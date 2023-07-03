from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from utils.paths_utils import database_credentials_path
from utils.file_utils import read_credentials

class Chat_dao:
    def __init__(self, data : List[List[str]]):
        """
        Initialize the Chat_dao class.

        Args:
            data (List[List[str]]): The chat history data.

        """
        db_credentials : dict = read_credentials(database_credentials_path)
        cluster : MongoClient = MongoClient(f"mongodb+srv://{db_credentials['username']}:{db_credentials['password']}@linkedin-bot.iac0yve.mongodb.net/?retryWrites=true&w=majority")
        mongo = cluster[db_credentials['db_name']]
        self.collection = mongo[db_credentials['db_name']]
        self.data : Dict[str, str] = {str(index) : " - ".join(name_text) for index, name_text in enumerate(data)}

    def insert(self) -> str:
        """
        Insert the chat history into the database.

        Returns:
            str: Message if successful, or an error message if an exception occurs.

        Raises:
            Exception: If an error occurs during the insertion.
        """
        try:
            self.collection.insert_one(self.data)
        except Exception as e:
            raise e
        return "Inserted successfully the chat history in the database"
    
    def insertion_allowed(self) -> bool:
        """
        Checks if the collection allows insertion.

        Returns:
            bool: True if insertion is allowed (collection is empty), False otherwise.

        Raises:
            Exception: If an error occurs while checking the collection.
        """
        try:
            document : Optional[Dict[str, Any]]|None = self.collection.find_one()
        except Exception as e:
            raise e
        return document is None
    
    def update(self):
        pass

    def delete(self):
        pass