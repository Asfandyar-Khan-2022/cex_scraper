"""system_module."""
import datetime
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument("--headless")
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
        self.url_list = []

    def load_and_accept_cookies(self) -> webdriver.Chrome:
        """
        Accept the cookies prompt.
        """
        self.url = 'https://uk.webuy.com/search/?stext=iphone%207%20plus'
        self.driver.get(self.url)
        time.sleep(10)
        accept_cookies_button = self.driver.find_element(By.XPATH,
        value='//*[@id="onetrust-accept-btn-handler"]')
        accept_cookies_button.click()
        time.sleep(1)
    
    def select_iphone(self):
        """
        Find the tick box responsible for grade a and click on it to only show grade a results.
        Do the same for grade b.
        """
        select_iphone = self.driver.find_element(By.XPATH,
        value='//*[@id="main"]/div/div/div[1]/div[2]/div/div[3]/div[1]/div/div[3]/div[3]/div/div/div/ul/li[1]/label/span[1]')
        select_iphone.click()
        time.sleep(2)
    
    def go_into_page_and_out(self):
        """
        The option that allows access to the image class is only made available after going into
        a device link and coming back out.
        """
        number_of_results = self.driver.find_element(By.XPATH, value='//*[@id="main"]/div/div/div[1]/div[2]/div/div[3]/div[2]/div[3]/div[1]/div/div[1]/p')
        number_of_results_only = int(number_of_results.text.split(' ')[0])
        parent = self.driver.find_elements(By.CSS_SELECTOR, value='a.line-clamp')
        index_of_result = parent[0].get_attribute('href').rfind('1')
        time.sleep(3)
        for i in range(1, number_of_results_only + 1):
            self.url_list.append(parent[0].get_attribute('href')[:index_of_result] + str(i))
        
        print(self.url_list)

        # for i in self.url_list:
        #     self.driver.execute_script("window.open('');") 
        #     self.driver.switch_to.window(self.driver.window_handles[1]) 
        #     self.driver.get(i)
        #     time.sleep(5)
        #     self.driver.close()
        #     self.driver.switch_to.window(self.driver.window_handles[0])
        # time.sleep(5)
        # print('here')
        # time.sleep(3)
        # self.driver.back()
        # time.sleep(100)


if __name__ == '__main__':
    start_crawling = Crawler()
    start_crawling.load_and_accept_cookies()
    start_crawling.select_iphone()
    start_crawling.go_into_page_and_out()