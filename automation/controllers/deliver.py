from typing import Self
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.paths_utils import write_message_classname, send_message_classname
from utils.logger_utils import logger

class Deliver_controller:
    def __init__(self, driver : webdriver, message : str):
        self.driver : webdriver = driver
        self.message : str = message
    
    def write_message(self) -> Self:
        """
        Writes the data generated by the LLM in the text box.

        Returns:
            The class instance for method chaining
        """
        try:
            div_message : object = self.driver.find_element(By.CLASS_NAME, write_message_classname)
            div_message.send_keys(self.message)
        except Exception as e:
            logger.error(f"Error when writing in the textbox: {e}")             
        return self
    
    def send_message(self) -> Self:
        """
        Click on the send button to send a message to a specific chat in LinkedIn.

        Returns:
            The class instance for method chaining
        """
        try:
            send_button : object = WebDriverWait(self.driver, 10)\
                .until(EC.element_to_be_clickable((By.CLASS_NAME, send_message_classname)))
            send_button.click()
        except Exception as e:
            logger.error(f"Error when sending the message: {e}")
        return self