from typing import List, Callable
from selenium import webdriver
from selenium.webdriver.common.by import By 
from utils.paths_utils import username_xpath, password_xpath
from utils.logger_utils import logger

class Login_controller:
    def __init__(self, driver : webdriver):
        self.driver : webdriver = driver
    
    def find_credential_xpaths(self) -> List[Callable]|None:
        try:
            username_field : str = self.driver.find_element(By.XPATH, username_xpath)
            password_field : str = self.driver.find_element(By.XPATH, password_xpath) 
            return username_field, password_field
        except Exception as e:
            logger.error(f"Error when getting the xpath: {e}")
        return None
    
    def update_input_fields(self, paths : List[Callable], linkedin_username : str, linkedin_password : str) -> None:
        username_path : Callable = None
        password_path : Callable = None
        try:
            username_path, password_path = paths
            username_path.send_keys(linkedin_username)
            password_path.send_keys(linkedin_password)
        except Exception as e:
            logger.error(f"Error when sending data to the input fields: {e}")            
        return None
