from typing import Deque, List, Dict, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By 
from utils.file_utils import read_content
from utils.paths_utils import selectors_path
from utils.logger_utils import logger
from data_access_objects.chat_dao import Chat_dao
from collections import deque

class Recruiter_messaging_controller(Chat_dao):
    def __init__(self, driver : webdriver, chat_history : List[List[str]]):
        super().__init__(chat_history)
        self.driver : webdriver = driver
        self.selectors : dict =  read_content(selectors_path)
        self.recruiter_message_lis : Deque = deque()
        self.first_message_li : object = None
    
    def fetch_new_messages(self) -> List[object]|None:
        messages_ul : object = self.driver.find_element(
                                                        By.XPATH, 
                                                        self.selectors["xpath"]["recruiter_messaging_xpath"])
        message_elements : List[object] = messages_ul.find_elements(
                                                                    By.TAG_NAME, 
                                                                    self.selectors["tag"]["list_item_tag"])
        self.first_message_li : object = message_elements[0]
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
    
    def has_similar_content_with_db_cluster(self, new_data) -> bool:
        old_data : Optional[Dict[str, Any]] = self.fetch_all()
        print(old_data)
        return True

    def add_head_message_from_messaging_inbox(self, message_li : object) -> Deque:
        return self.recruiter_message_lis.appendleft(message_li)
        