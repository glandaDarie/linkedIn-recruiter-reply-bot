from typing import Match, Self
from re import search, MULTILINE
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.regex_utils import pattern_name
from utils.logger_utils import logger
from utils.file_utils import read_content
from utils.paths_utils import selectors_path

class Account_name_controller:
    def __init__(self, xpath : str, driver : webdriver):
        self.xpath : str = xpath
        self.driver : webdriver = driver
        self.name : str|None = None
        self.selectors : dict = read_content(selectors_path)["css"]

    def build_name(self) -> Self:
        fullname_div : object = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, self.selectors["fullname_css"]))
        )
        data : str = fullname_div.text
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