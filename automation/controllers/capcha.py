from selenium import webdriver
from selenium.webdriver.common.by import By 
from utils.paths_utils import capcha_verification_xpath
from utils.logger_utils import logger
import easygui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Capcha_controller:
    def __init__(self, driver: webdriver):
        """
        Initialize the Capcha_controller class.
            
        Args:
            driver (webdriver): The webdriver for scrapping the elements from the page"
        """  
        self.driver : webdriver = driver
    
    def capcha_appeard(self) -> bool:
        """
        Check if the CAPTCHA verification appears on the page.

        Returns:
            bool: True if the CAPTCHA verification appears, False otherwise.
        """
        element: object | None = None
        try:
            self.driver.switch_to.frame(iframe_present)
            iframe_present : object = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='arkose']/div/iframe"))
            )
            self.driver.switch_to.frame(iframe_present)
            element: object = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, capcha_verification_xpath))
            )
        except Exception as e:
            logger.info(f"Captcha is not present, continue: {e}")
        return element is not None and element.text == "Verification"

    def manual_completion(self, message : str = "Press finish once you complete the CAPCHA.") -> bool: 
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

