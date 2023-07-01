from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By 
from utils.paths_utils import username_xpath, password_xpath, login_xpath 
from utils.logger_utils import logger

class Login_controller:
    def __init__(self, driver : webdriver):
        self.driver : webdriver = driver
    
    def find_credential_xpaths(self) -> List[object]|None:
        try:
            username_field : str = self.driver.find_element(By.XPATH, username_xpath)
            password_field : str = self.driver.find_element(By.XPATH, password_xpath) 
            return username_field, password_field
        except Exception as e:
            logger.error(f"Error when getting the xpath: {e}")
        return None
    
    def update_input_fields(self, paths : List[object], linkedin_username : str, linkedin_password : str) -> None:
        username_element : object = None
        password_element : object = None
        try:
            username_element, password_element = paths
            username_element.send_keys(linkedin_username)
            password_element.send_keys(linkedin_password)
        except Exception as e:
            logger.error(f"Error when sending data to the input fields: {e}")            
        return None

    def login_to_linkedin(self) -> None:
        try:
            self.driver.find_element(By.XPATH, login_xpath).click()
        except Exception as e:
            logger.error(f"Error when trying to click on the submit button: {e}")  