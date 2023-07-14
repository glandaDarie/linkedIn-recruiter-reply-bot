from typing import Match
from re import search, MULTILINE
from selenium import webdriver
from selenium.webdriver.common.by import By 
from time import sleep
from utils.regex_utils import pattern_name
from utils.logger_utils import logger

class Account_name_controller:
    def __init__(self, xpath : str, driver : webdriver):
        self.xpath : str = xpath
        self.driver : webdriver = driver
        self.name : str|None = None

    def build_name(self): 
        name_div : object = self.driver.find_element(By.XPATH, self.xpath)
        data : str = name_div.text
        self.name : str = self.extract_name_from_data(data)
        if self.name is None:
            logger.error(f"Error when trying to get the name of the user account from linkedin")
            return None
        return self

    def extract_name_from_data(self, data : str) -> str|None:
        match : Match = search(pattern_name, data, MULTILINE)
        if not match:
            return None
        name : str = match.group(1)
        return name