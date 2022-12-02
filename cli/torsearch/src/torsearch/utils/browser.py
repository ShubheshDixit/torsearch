from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import Optional

options = Options()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])


browser: Optional[webdriver.Chrome] = None


def get_browser():
    global browser
    if browser is None:
        browser = webdriver.Chrome(options=options)
    # else:
    #     browser.quit()
    #     browser = webdriver.Chrome(options=options)
    return browser
