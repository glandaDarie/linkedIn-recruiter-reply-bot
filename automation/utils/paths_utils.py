import os

current_directory : str = os.getcwd()
linkedin_credentials_path : str = os.path.join(current_directory, "files", "linkedin_credentials.json")
database_credentials_path : str = os.path.join(current_directory, "files", "database_credentials.json")
llm_api_token_path : str = os.path.join(current_directory, "files", "llm_api_tokens.json")
selectors_path : str = os.path.join(current_directory, "files", "selectors.json")
personal_data_path : str = os.path.join(current_directory, "files", "personal_data.txt")

username_xpath : str = "//input[@name = 'session_key']"
password_xpath : str = "//input[@name = 'session_password']"
login_xpath : str = "//button[@type = 'submit']"
messages_xpath : str = "//*[@id='global-nav']/div/nav/ul/li[4]/a"
head_message : str = "//*[@id='message-list-ember8']/ul/li[]/div/div/div/div/p"
messages_list_xpath : str = "//*[@id='message-list-ember8']/ul" 
scrollable_xpath : str = "//*[@id='message-list-ember8']"
capcha_verification_xpath : str = "//*[@id='home_children_heading']"
user_account_fullname_xpath : str = "//*[@id='ember18']"
send_message_xpath : str = "//*[@id='msg-form-ember692']/div[3]/div/div[1]/div[1]"
