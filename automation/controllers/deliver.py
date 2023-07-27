from typing import Self
from selenium import webdriver
from selenium.webdriver.common.by import By 
from utils.paths_utils import send_message_xpath 
from utils.logger_utils import logger

class Deliver_controller:
    def __init__(self, driver : webdriver, message : str):
        self.driver : webdriver = driver
        self.message : str = message
    
    def write_message(self) -> Self:
        try:
            div_message : object = self.driver.find_element(By.CLASS_NAME, "msg-form__contenteditable")
            div_message.send_keys(self.message)
        except Exception as e:
            logger.error(f"Error when writing in the textbox: {e}")             
        return self
    
    def send_message(self) -> Self:
        return self