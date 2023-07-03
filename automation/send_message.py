from typing import List
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service   
from webdriver_manager.chrome import ChromeDriverManager
from utils.option_utils import options, linkedin_url
from utils.file_utils import read_credentials, encrypted_credentials, \
    encrypt_credentials, write_encrypted_credentials
from utils.paths_utils import linkedin_credentials_path
from utils.crypto_utils import decrypt_aes
from controllers.login import Login_controller
from controllers.message import Message_controller
from controllers.capcha import Capcha_controller
from data_access_objects.chat_dao import Chat_dao
from utils.logger_utils import logger

if __name__ == "__main__":
    driver : webdriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(linkedin_url)
    driver.maximize_window()
    if not encrypted_credentials(linkedin_credentials_path):
        credentials_encrypted : dict = encrypt_credentials(linkedin_credentials_path)
        write_encrypted_credentials(linkedin_credentials_path, credentials_encrypted)
    linkedin_credentials : dict = read_credentials(linkedin_credentials_path)
    linkedin_username : str = decrypt_aes(linkedin_credentials['username'], linkedin_credentials['key']).decode('utf-8')
    linkedin_password : str = decrypt_aes(linkedin_credentials['password'], linkedin_credentials['key']).decode('utf-8')
    login_controller : Login_controller = Login_controller(driver=driver)
    credential_paths: List[object] = login_controller.find_credential_xpaths()
    login_controller.update_input_fields(paths=credential_paths, linkedin_username=linkedin_username, linkedin_password=linkedin_password)
    login_controller.login_to_linkedin() 
    capcha_controller : Capcha_controller = Capcha_controller(driver)
    sleep(5)
    if capcha_controller.capcha_appeard():
        capcha_controller.manual_completion()
    sleep(5)
    message_controller : Message_controller = Message_controller(driver=driver) 
    url_messages : str|None = message_controller.get_messages_url()
    if url_messages is None:
        logger.error("Error when providing the url")
        sys.exit(1)
    driver.get(url_messages)
    chat : List[List[str]] = message_controller.fetch_percentwise_chat_history()
    chat_dao : Chat_dao = Chat_dao(chat) 
    if not chat_dao.insertion_allowed():
        logger.info("Can't insert in the db, data is present already")
    else:
        result : None|str = chat_dao.insert()
        logger.info(result)