from pprint import pprint
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os

from cache.cache import cache


def video_resolver(obj, info):
    return cache.get('video_src')


def get_video_src_and_set_cache(obj, info):
    video_src = getVideoSrc()
    cache.set('video_src', video_src)
    return video_src


def getVideoSrc():
    options = ChromeOptions()
    options.headless = True
    if os.getenv('IN_DOCKER') is not None:
        options.binary_location = '/usr/bin/google-chrome'
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-dev-shm-usage')
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
