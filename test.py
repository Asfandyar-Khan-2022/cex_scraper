import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

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
        self.driver = webdriver.Chrome(options=chrome_options)
        self.url = 'https://mars.nasa.gov/msl/mission/weather/'
        self.row_data = []


    def grab_data(self):
        """
        Accept the cookies prompt.
        """
        self.driver.get(self.url)
        time.sleep(3)
        data = self.driver.find_elements(By.XPATH, value='//*[@id="weather_observation"]/tbody')
        for i in data:
            self.row_data.append(i.text)
        test = self.row_data
        self.row_data = test[0].split('\n')
        time.sleep(1)
        self.export_json()

    def export_json(self):
        with open('mars.json', 'w') as f:
            json.dump(self.row_data, f)

if __name__ == '__main__':
    start_crawling = Crawler()
    start_crawling.grab_data()