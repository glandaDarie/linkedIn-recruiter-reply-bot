import os

current_directory : str = os.getcwd()
linkedin_credentials_path : str = os.path.join(current_directory, "files", "linkedin_credentials.json")

username_xpath : str = "//input[@name = 'session_key']"
password_xpath : str = "//input[@name = 'session_password']"
login_xpath : str = "//button[@type = 'submit']"
messages_xpath : str = "//*[@id='global-nav']/div/nav/ul/li[4]/a"
specific_message_xpath : str = "//*[@id='ember33']"
head_message : str = "//*[@id='message-list-ember8']/ul/li[]/div/div/div/div/p"

# //*[@id="message-list-ember8"]/ul/li[22]/div/div[2]/div/div/p
# //*[@id="message-list-ember8"]/ul/li[21]/div[1]/div[2]/div/div/p
# //*[@id="message-list-ember8"]/ul/li[20]/div/div[2]/div/div/p