import os

current_directory : str = os.getcwd()
linkedin_credentials_path : str = os.path.join(current_directory, "files", "linkedin_credentials.json")

username_xpath : str = "//input[@name = 'session_key']"
password_xpath : str = "//input[@name = 'session_password']"