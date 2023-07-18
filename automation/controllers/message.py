from typing import List, Tuple, Match
from utils.paths_utils import messages_xpath, head_message, \
    messages_xpath, messages_list_xpath, scrollable_xpath
from selenium import webdriver
from selenium.webdriver.common.by import By 
from utils.logger_utils import logger
from utils.regex_utils import sender_name_pattern
import re
from math import ceil
from time import sleep

class Message_controller:
    def __init__(self, driver : webdriver, profile_name : str):
        """
        Initialize the Message_controller class.

        Args:
            driver (webdriver): The webdriver used for web scrapping
            profile_name (str): The users profile name for distinction between him and the recruiter
        """
        self.driver : webdriver = driver
        self.profile_name : str = profile_name

    def get_messages_url(self) -> str | None:
        """
        Get the URL of the messages page.

        Returns:
            str|None: The URL of the messages page, or None if an error occurs.
        """
        try:
            messages_element : object = self.driver.find_element(By.XPATH, messages_xpath)
            messages_href : str = messages_element.get_attribute("href")
        except Exception as e:
            logger.error(f"Error when getting the url: {e}")
            return None
        return messages_href
    
    def fetch_percentwise_chat_history(self, chat_percentage : int = 20, pixels_batch : int = 300) -> List[List[str]]:
        """
        Fetches the percent-wise chat history from the messages page.

        Args:
            chat_percentage (int): The percentage of the chat history to keep (range 10-100). Default is 40% 
            pixels_batch (int): The number of pixels to scroll in each batch. Default is 300.

        Returns:
            List[List[str]]: A list containing the name of the sender and the chat history messages. 
        """
        sleep(4)
        chat_history: List[List[str]] = []
        assert chat_percentage >= 10 and chat_percentage <= 100, "Invalid chat_percentage \
            value. Must be between 10 and 100." 
        try:
            messages_div: object = self.driver.find_element(By.XPATH, messages_list_xpath) 
            scrollable_div: object = self.driver.find_element(By.XPATH, scrollable_xpath)
            snapshot_pixel_batch : int = pixels_batch
            prev_location_table_height, current_location_table_height = 1, 0
            while prev_location_table_height != current_location_table_height:
                prev_location_table_height : int = self.driver.execute_script("return arguments[0].scrollTop", scrollable_div)
                self.driver.execute_script(f"arguments[0].scrollTop -= {snapshot_pixel_batch}", scrollable_div)
                snapshot_pixel_batch += pixels_batch
                sleep(4)
                current_location_table_height : int = self.driver.execute_script("return arguments[0].scrollTop", scrollable_div)
            messages_li: List[object] = messages_div.find_elements(By.TAG_NAME, "li")   
            sleep(3) 
            sender_name : str|None = None
            for index, message_li in enumerate(messages_li):
                class_name : str = message_li.get_attribute("class").strip()
                if class_name == "msg-s-message-list__event clearfix":
                    result : Tuple[str] | Exception = self.get_senders_name_and_message(sender_name, message_li, index)
                    if not isinstance(result, tuple):
                        logger.error(f"Error when fetching data: {result}")
                    sender_name, sender_message = result
                    if sender_name == self.profile_name:
                        sender_name = f"{sender_name} (me)"
                    chat_history.append([sender_name, sender_message])
            start_index : int = len(chat_history) - ceil(chat_percentage/100 * len(chat_history))
            chat_history : List[List[str]] = chat_history[start_index:]
        except Exception as e:
            logger.error(f"Error when fetching messages: {e}")
            return None
        return chat_history

    def get_senders_name_and_message(self, sender_name: str | None, message_li: object, index: int) -> Tuple[str] | Exception:
        """
        Helper method to extract the sender's name and message from a message list item.

        Args:
            sender_name (str | None): The name of the message sender.
            message_li (object): The message list item element.
            index (int): The index of the current element position.

        Returns:
            Tuple[str] | Exception: A tuple containing the sender's name and message, or an Exception if an error occurs.
        """
        try:
            message_tags: List[object] = message_li.find_elements(By.XPATH, "./*")
            sender_message: str = re.split("PM|AM", message_tags[-1 if index == 0 else -2].text)[-1].strip()
            if index == 0:
                match: Match[str] | None = re.search(sender_name_pattern, message_tags[-1].text)
            else:
                match: Match[str] | None = re.search(sender_name_pattern, message_tags[-2].text)
            sender_name: str = match.group(1) if match else None
        except Exception as e:
            logger.error(f"Error when fetching the chat history: {e}")
            return e
        return sender_name, sender_message

    def fetch_last_k_messages_from_chat_history(self, k : int = 3) -> List[str]|None:
        """
        Fetch the last k messages from the chat history.

        Args:
            k (int): The number of messages to fetch. Default is 3.

        Returns:
            List[str]|None: A list containing the last k messages, or None if an error occurs.
        """
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