"""system_module."""
import datetime
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("start-maximised")

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])


class Crawler:
    """
    This class is used to gather Iphone price data.
    """


    def __init__(self):
        """
        See help(Crawler) for accurate signature
        """
        self.driver = driver = webdriver.Chrome(options=chrome_options)
        self.url = 'https://uk.webuy.com/search?stext=iphone%207%20plus'
        self.phones_names_list = []
        self.phones_price_list = []
        self.image_url_list = []


if __name__ == '__main__':
    start_crawling = Crawler()
