from bs4 import BeautifulSoup
import requests as req
from pprint import pprint
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By



def video_resolver(obj, info):
    options = ChromeOptions()
    options.headless = True
    options.binary_location = '/usr/bin/google-chrome'
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')

    driver = Chrome(ChromeDriverManager().install(), options=options)
    driver.get('https://www.zhihu.com/question/378598799/answer/1126026947')

    try:
        button = driver.find_element(By.CLASS_NAME, "Modal-closeButton")
        button.click()

        element = driver.find_element(By.TAG_NAME, "iframe")
        pprint(element)

        driver.switch_to.frame(element)
        video = driver.find_element(By.TAG_NAME, "video")
        pprint(video)
        src = video.get_attribute('src')
        return src

    finally:
        # always close the browser
        driver.quit()