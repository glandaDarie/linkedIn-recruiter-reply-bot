from selenium.webdriver.chrome.options import Options

options = Options() 
options.add_experimental_option("detach", True)

url_linkedin : str = "https://www.linkedin.com/checkpoint/lg/sign-in-another-account"