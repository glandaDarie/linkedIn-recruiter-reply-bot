from time import sleep
from typing import List, Callable
from utils.paths_utils import messages_xpath, head_message, messages_div
from selenium import webdriver
from selenium.webdriver.common.by import By 
from utils.logger_utils import logger
import re

class Message_controller:
    def __init__(self, driver : webdriver):
        self.driver = driver

    def get_messages_url(self) -> str|None:
        try:
            messages_element : Callable = self.driver.find_element(By.XPATH, messages_xpath)
            messages_href : str = messages_element.get_attribute("href")
        except Exception as e:
            logger.error(f"Error when getting the url: {e}")
            return None
        return messages_href
    
    def fetch_all_messages(self) -> List[str]:
        sleep(2)
        message_history : List[str] = []
        try:
            div_messages : object = self.driver.find_element(By.XPATH, messages_div)
            messages_li : List[object] = div_messages.find_elements(By.TAG_NAME, "li") 
            indices_messages : List[int] = list(range(1, len(messages_li) + 1))
            indices_messages_li : List[object] = [
                    indices_messages[index] for index, message_li in enumerate(messages_li) if \
                    message_li.get_attribute("class").strip() == "msg-s-message-list__event clearfix"
            ]
            convo_indices : List[List[int]] = []
            for index_message in indices_messages_li:
                _messages_div =  f"{messages_div}/li[{index_message}]".strip()
                div_messages : object = self.driver.find_element(By.XPATH, _messages_div)
                tags : List[object] = div_messages.find_elements(By.XPATH, "./*")
                convo_index : int = [
                        index for index, t in enumerate(tags) 
                              if re.search(r"msg-s-event-listitem\s{4,}", t.get_attribute("class"))
                ][0]
                convo_indices.append(convo_index)
            print(f"Convo indicies: {convo_indices}")
        except Exception as e:
            logger.error(f"Error when the text from the p tag: {e}")
            return None
        return message_history

    def fetch_last_k_messages_from_message_queue(self, k : int = 3) -> List[str]|None:
        sleep(2) 
        message_elements : List[str] = []
        try:
            for index in list(range(23-k, 23)):
                message_xpath : str = f"{head_message[:37]}{index}{head_message[37:]}" 
                message_element : Callable = self.driver.find_element(By.XPATH, message_xpath)
                message_elements.append(message_element.text)
        except Exception as e:
            logger.error(f"Error when the text from the p tag: {e}")
            return None
        return message_elements