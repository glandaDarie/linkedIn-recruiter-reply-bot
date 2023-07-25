from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from utils.paths_utils import database_credentials_path
from utils.file_utils import read_content

class Chat_dao:
    def __init__(self):
        """
        Initialize the Chat_dao class.
        """  
        db_credentials : dict = read_content(database_credentials_path)
        uri : str = f"mongodb+srv://{db_credentials['username']}:{db_credentials['password']}@linkedin-replier-cluste.qcijzcn.mongodb.net/?retryWrites=true&w=majority"
        cluster : MongoClient = MongoClient(uri)
        mongo = cluster[db_credentials['db_name']]
        self.collection = mongo[db_credentials['db_name']]

    def insert(self, data : Dict[str, str]) -> str:
        """
        Insert the chat history into the database.

        Args:
            data (Dict[str, str]): The data to be inserted in the collection.

        Returns:
            str: Message if successful, or an error message if an exception occurs.

        Raises:
            Exception: If an error occurs during the insertion.
        """
        try:
            self.collection.insert_one(data)
        except Exception as e:
            raise e
        return "Inserted successfully the chat history in the database"
    
    def fetch_all(self) -> Optional[Dict[str, Any]]:
        """
        Fetch all documents from the collection.

        Returns:
            Optional[Dict[str, Any]]: The fetched document if it exists, None otherwise.

        Raises:
            Exception: If an error occurs while fetching the documents.
        """
        try:
            document : Optional[Dict[str, Any]]|None = self.collection.find_one()
            first_item : Dict[str, Any] = next(iter(document))
            document.pop(first_item)
        except Exception as e:
            raise e
        return document

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

    def update(self, old_data: Optional[Dict[str, Any]], new_data : Optional[Dict[str, Any]]) -> str:
        """
        Update the chat history in the database with new data.

        Args:
            old_data (Optional[Dict[str, Any]]): The old chat history data to be updated.
            new_data (Optional[Dict[str, Any]]): The new chat history data 

        Returns:
            str: Message indicating the successful update.

        Raises:
            Exception: If an error occurs during the update.
        """
        try:
            new_data : Dict[str, Dict[str, Any]] = {"$set": new_data}
            self.collection.update_one(old_data, new_data)
        except Exception as e:
            raise e
        return "Updated successfully the chat history in the database"

    def delete_all_the_content(self) -> str:
        """
        Delete all the content from the collection.

        Returns:
            str: Message indicating the successful deletion.

        Raises:
            Exception: If an error occurs during the deletion.
        """
        try:
            self.collection.delete_many({})
        except Exception as e:
            raise e
        return "Deleted successfully all the chat history from the database"