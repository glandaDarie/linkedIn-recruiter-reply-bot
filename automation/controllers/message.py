from time import sleep
from typing import List, Tuple
from utils.paths_utils import messages_xpath, head_message, messages_div
from selenium import webdriver
from selenium.webdriver.common.by import By 
from utils.logger_utils import logger

class Message_controller:
    def __init__(self, driver : webdriver):
        self.driver : webdriver = driver

    def get_messages_url(self) -> str|None:
        try:
            messages_element : object = self.driver.find_element(By.XPATH, messages_xpath)
            messages_href : str = messages_element.get_attribute("href")
        except Exception as e:
            logger.error(f"Error when getting the url: {e}")
            return None
        return messages_href
    
    def fetch_all_chat_history(self, pixels_batch : int = 400) -> List[str]:
        sleep(2)
        chat_history: List[List[str, str]] = []
        try:
            div_messages: object = self.driver.find_element(By.XPATH, messages_div)
            messages_li: List[object] = div_messages.find_elements(By.TAG_NAME, "li")    
            scrollable_div: object = self.driver.find_element(By.XPATH, "//*[@id='message-list-ember8']")
            snapshot_pixel_batch : int = pixels_batch
            prev_location_table_height, current_location_table_height = 1, 0
            while prev_location_table_height != current_location_table_height:
                prev_location_table_height : int = self.driver.execute_script("return arguments[0].scrollTop", scrollable_div)
                self.driver.execute_script(f"arguments[0].scrollTop -= {snapshot_pixel_batch}", scrollable_div)
                snapshot_pixel_batch += pixels_batch
                sleep(3)
                current_location_table_height : int = self.driver.execute_script("return arguments[0].scrollTop", scrollable_div)
            sleep(3) 
            for message_li in messages_li:
                class_name : str = message_li.get_attribute("class").strip()
                if class_name == "msg-s-message-list__event clearfix":
                    name, message = self.get_senders_name_and_message(message_li)
                    chat_history.append(message_li.text)                    
        except Exception as e:
            logger.error(f"Error when fetching messages: {e}")
            return None
        return chat_history
    
    def get_senders_name_and_message(self, message_li : object) -> Tuple[str, str]:
        tags : List[object] = message_li.find_elements(By.XPATH, "./*")
        for index, tag in enumerate(tags):
            print(f"{index}) Information: {tag.text}")
        return "sender_name", "sender_message" 

    def fetch_last_k_messages_from_message_queue(self, k : int = 3) -> List[str]|None:
        sleep(2) 
        message_elements : List[str] = []
        try:
            for index in list(range(23-k, 23)):
                message_xpath : str = f"{head_message[:37]}{index}{head_message[37:]}" 
                message_element : object = self.driver.find_element(By.XPATH, message_xpath)
                message_elements.append(message_element.text)
        except Exception as e:
            logger.error(f"Error when the text from the p tag: {e}")
            return None
        return message_elements