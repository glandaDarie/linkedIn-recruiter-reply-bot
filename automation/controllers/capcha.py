from selenium import webdriver
from selenium.webdriver.common.by import By 
from utils.paths_utils import capcha_verification_xpath
from utils.logger_utils import logger
import easygui

class Capcha_controller:
    def __init__(self, driver: webdriver):
        self.driver : webdriver = driver
    
    def capcha_appeard(self) -> bool:
        """
        Check if the CAPTCHA verification appears on the page.

        Returns:
            bool: True if the CAPTCHA verification appears, False otherwise.
        """
        try:
            self.driver.find_elements(By.XPATH, capcha_verification_xpath)
        except Exception as e:
            logger.info(f"Capcha is not present, continue: {e}")
            return False
        return True
    
    def manual_completion(self, message : str = "Press finish once you completed the CAPCHA.") -> bool: 
        """
        Prompt the user to manually complete the CAPTCHA.

        Args:
            message (str): The message to display in the dialog box. Default is "Press 'Finish' once you have completed the CAPTCHA."

        Returns:
            bool: True after the user completes the CAPTCHA.

        Note:
            This method will display a pop-up dialog box using easygui library, instructing the user to manually complete the CAPTCHA.
            It will wait for the user to click the "Finish" button, and then prompt for an additional input from the user using the input() function.
        """       
        easygui.msgbox(message, "Text Popup", "Finish")

