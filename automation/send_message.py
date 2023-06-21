from typing import List, Callable
from selenium import webdriver
from selenium.webdriver.chrome.service import Service   
from webdriver_manager.chrome import ChromeDriverManager
from utils.option_utils import options, linkedin_url
from utils.file_utils import read_credentials, encrypted_credentials, encrypt_credentials, write_encrypted_credentials
from utils.paths_utils import linkedin_credentials_path
from utils.crypto_utils import decrypt_aes
from controllers.login import Login_controller

if __name__ == "__main__":
    driver : webdriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(linkedin_url)
    driver.maximize_window()
    if not encrypted_credentials(linkedin_credentials_path):
        credentials_encrypted : dict = encrypt_credentials(linkedin_credentials_path)
        write_encrypted_credentials(linkedin_credentials_path, credentials_encrypted)
    dict_credentials = read_credentials(linkedin_credentials_path)
    linkedin_username : str = decrypt_aes(dict_credentials["username"], dict_credentials["key"]).decode("utf-8")
    linkedin_password : str = decrypt_aes(dict_credentials["password"], dict_credentials["key"]).decode("utf-8")

    login_controller = Login_controller(driver=driver)
    credential_paths: List[Callable] = login_controller.find_credential_xpaths()
    login_controller.update_input_fields(paths=credential_paths, linkedin_username=linkedin_username, linkedin_password=linkedin_password)