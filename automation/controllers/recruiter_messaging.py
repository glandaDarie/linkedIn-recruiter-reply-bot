from typing import Deque, List, Dict, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By 
from utils.file_utils import read_content
from utils.paths_utils import selectors_path
from utils.logger_utils import logger
from data_access_objects.chat_dao import Chat_dao
from collections import deque

class Recruiter_messaging_controller(Chat_dao):
    def __init__(self, driver : webdriver, new_chat_history : List[List[str]]):
        """
        Initialize the Recruiter_messaging_controller class.

        Args:
            driver (webdriver): The Selenium webdriver instance.
            new_chat_history (List[List[str]]): The new chat history data.
        """
        super().__init__(new_chat_history)
        self.driver : webdriver = driver
        self.new_chat_history : List[List[str]] = new_chat_history
        self.selectors : dict =  read_content(selectors_path)
        self.recruiter_message_lis : Deque = deque()
        self.first_message_li : object = None
        self.second_message_li : object = None
    
    def fetch_new_messages(self) -> List[object]|None:
        """
        Fetches the new messages from the messaging inbox.

        Returns:
            List[object] | None: A list of message elements if messages are found, None otherwise.
        """
        messages_ul : object = self.driver.find_element(
                                                        By.XPATH, 
                                                        self.selectors["xpath"]["recruiter_messaging_xpath"])
        message_elements : List[object] = messages_ul.find_elements(
                                                                    By.TAG_NAME, 
                                                                    self.selectors["tag"]["list_item_tag"])
        self.first_message_li : object = message_elements[1]
        for index, message_element in enumerate(message_elements):
            try:
                class_name : str = message_element.find_element(
                                                        By.TAG_NAME, 
                                                        self.selectors["tag"]["h3_tag"])\
                                                        .get_attribute("class")
                if "t-bold" in class_name:
                    self.recruiter_message_lis.append(message_element)
            except Exception as e:
                logger.info(f"{index}: has no element: {e}")
        return self.recruiter_message_lis
    
    def has_similar_content_with_db_collection(self) -> bool:
        """
        Checks if the new chat history content is similar to the existing chat history in the database.

        Returns:
            bool: True if the content is similar, False otherwise.
        """
        try:
            old_chat_history : Optional[Dict[str, Any]] = self.fetch_all()            
            str_old_chat_history : str = "\n".join(old_chat_history.values())
            str_new_chat_history : str = "\n".join([f"{sentence[0]} - {sentence[1]}" for sentence in self.new_chat_history])
            if str_old_chat_history == str_new_chat_history:
                return True
        except Exception as e:
            logger.info(f"Error when trying to fetch the data from the mongo cluster: {e}")
        return False

    def add_head_message_from_messaging_inbox(self) -> Deque:
        """
        Adds the first message from message list item to the head of the recruiter_message_lis deque.

        Returns:
            Deque: The updated recruiter_message_lis deque.
        """
        self.recruiter_message_lis.appendleft(self.first_message_li)