import random
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from undetected_chromedriver import Chrome
from selenium.webdriver.firefox.options import Options

from Utils.logger import logger
from constants import profile_path


class Browser:
    def __init__(self, ):
        self.driver = None

    def get_source(self, url):
        page_source = None
        logger.info(f"Sending request to ({url})")
        try:
            self.get_url(url)
            time.sleep(random.randint(15, 35))
            page_source = self.driver.page_source
        except  Exception as e:
            logger.error(f"Request Failed ")
            page_source = None
        finally:
            return page_source

    def get_soup(self, url):
        response_text = self.get_source(url)
        if response_text is not None:
            soup = BeautifulSoup(response_text, "html.parser")
            return soup
        else:
            return None

    def get_current_soup(self):
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def get_url(self, url):
        self.driver.get(url)

    def close_driver(self):
        self.driver.close()


class ChromeBrowser(Browser):
    def __init__(self):
        super().__init__()
        self.driver = Chrome()


class FirefoxBrowser(Browser):

    def __init__(self):
        super().__init__()
        self.firefox_options = Options()
        self.firefox_options.profile = webdriver.FirefoxProfile(profile_path)
        self.driver = webdriver.Firefox(options=self.firefox_options)
