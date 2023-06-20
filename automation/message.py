from typing import Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service    
from webdriver_manager.chrome import ChromeDriverManager
from utils.option_utils import options, url_linkedin
from utils.file_utils import read_credentials, encrypted_credentials, encrypt_credentials
from utils.paths_utils import linkedin_credentials_path
from utils.crypto_utils import decrypt_aes

if __name__ == "__main__":
    driver : webdriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url_linkedin)
    driver.maximize_window()

    if not encrypted_credentials(linkedin_credentials_path):
        encrypt_credentials(linkedin_credentials_path)

    json_credentials = read_credentials(linkedin_credentials_path)
    linkedin_username : str = decrypt_aes(json_credentials["username"], json_credentials["key"]).decode("utf-8")
    linkedin_password : str = decrypt_aes(json_credentials["password"], json_credentials["key"]).decode("utf-8")

