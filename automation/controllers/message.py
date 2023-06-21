from time import sleep
from typing import List, Callable
from utils.paths_utils import messages_xpath, head_message
from selenium import webdriver
from selenium.webdriver.common.by import By 
from utils.logger_utils import logger

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
    
    def fetch_last_k_messages_from_message_queue(self, k : int = 3) -> List[str]|None:
        sleep(2) 
        message_elements : List[str] = []
        try:
            for index in list(range(23-k, 23)):
                message_xpath : str = f"{head_message[:37]}{index}{head_message[37:]}" 
                print(f"message_xpath: {message_xpath}")
                message_element : Callable = self.driver.find_element(By.XPATH, message_xpath)
                message_elements.append(message_element.text)
        except Exception as e:
            logger.error(f"Error when the text from the p tag: {e}")
            return None
        return message_elements