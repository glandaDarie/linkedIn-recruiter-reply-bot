from typing import List, Dict, Any, Optional
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service   
from webdriver_manager.chrome import ChromeDriverManager
from utils.option_utils import options, linkedin_url
from utils.file_utils import read_content, encrypted_credentials, \
    encrypt_credentials, write_encrypted_credentials
from utils.paths_utils import linkedin_credentials_path, user_account_fullname_xpath
from utils.crypto_utils import decrypt_aes
from controllers.login import Login_controller
from controllers.message import Message_controller
from controllers.capcha import Capcha_controller
from controllers.account_name import Account_name_controller
from controllers.recruiter_messaging import Recruiter_messaging_controller
from data_access_objects.chat_dao import Chat_dao
from utils.logger_utils import logger
from recruiter_text_replier.llm_reply_factory import LLM_Reply_factory
from controllers.deliver import Deliver_controller

if __name__ == "__main__":
    driver : webdriver = webdriver.Chrome(service=Service(ChromeDriverManager("114.0.5735.90").install()), options=options)
    driver.get(linkedin_url)
    driver.maximize_window()
    if not encrypted_credentials(linkedin_credentials_path):
        credentials_encrypted : dict = encrypt_credentials(linkedin_credentials_path)
        write_encrypted_credentials(linkedin_credentials_path, credentials_encrypted)
    linkedin_credentials : dict = read_content(linkedin_credentials_path)
    linkedin_username : str = decrypt_aes(linkedin_credentials["username"], linkedin_credentials["key"]).decode("utf-8")
    linkedin_password : str = decrypt_aes(linkedin_credentials["password"], linkedin_credentials["key"]).decode("utf-8")
    login_controller : Login_controller = Login_controller(driver=driver)
    credential_paths: List[object] = login_controller.find_credential_xpaths()
    login_controller.update_input_fields(paths=credential_paths, 
                                         linkedin_username=linkedin_username, 
                                         linkedin_password=linkedin_password)
    login_controller.login_to_linkedin() 
    capcha_controller : Capcha_controller = Capcha_controller(driver=driver)
    if capcha_controller.capcha_appeard():
        capcha_controller.manual_completion()
    sleep(5)
    account_name_controller : Account_name_controller = Account_name_controller(
        xpath=user_account_fullname_xpath, 
        driver=driver
    )
    account_profile_name : str = account_name_controller.build_name().name
    sleep(4)
    message_controller : Message_controller = Message_controller(driver=driver,
                                                                 profile_name=account_profile_name) 
    url_messages : str | None = message_controller.get_messages_url()
    if url_messages is None:
        print("Error when providing the url")
        sys.exit(1)
    driver.get(url_messages)
    chat : List[List[str]] = message_controller.fetch_percentwise_chat_history()
    chat : Dict[str, str] = message_controller.format_chat_for_processing(chat=chat)
    if chat is None:
        print("Chat is empty, can't fetch data")
        sys.exit(1)
    sleep(6)
    recruiter_messaging_controller : Recruiter_messaging_controller = \
        Recruiter_messaging_controller(driver=driver, new_chat_history=chat)
    recruiter_messages_objects : List[object] = recruiter_messaging_controller.fetch_new_messages()
    if not recruiter_messaging_controller.has_similar_content_with_db_collection():
        recruiter_messaging_controller.add_head_message_from_messaging_inbox()
    chat_dao : Chat_dao = Chat_dao() 
    chats : List[List[List[str]]] = []    
    for index, message_li in enumerate(list(recruiter_messaging_controller.recruiter_message_lis)):
        if index == 0: 
            chats.append(chat)
        else:
            message_li.click()
            sleep(6)
            chat : List[List[str]] = message_controller.fetch_percentwise_chat_history()
            if chat is None:
                print("Chat is empty, can't fetch data")
                sys.exit(1)
            chats.append(chat)
        if not chat_dao.insertion_allowed():
            logger.info("Can't insert in the db, data is present already")
            old_data : Optional[Dict[str, Any]] = chat_dao.fetch_all()
            response : str = chat_dao.delete_all_the_content()
            logger.info(response)    
        response : str = chat_dao.insert(chats[index])
        logger.info(response)    
        chat : str = "\n".join([f"{key}) {value}" for key, value in chat.items()])
        try: 
            llm_reply_factory : LLM_Reply_factory = LLM_Reply_factory(llm_name="<open_ai>")
            llm : object | NotImplementedError = llm_reply_factory.create_llm()
            response : str = llm.predict(query=chat)
            deliver_controller : Deliver_controller = Deliver_controller(driver=driver, message=response)
            # print(f"Response: {response}")
            deliver_controller.write_message()
        except Exception as e:
            logger.error(f"Error with langchain implementation: {e}")