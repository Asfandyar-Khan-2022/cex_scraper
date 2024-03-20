"""system_module."""
import datetime
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.chrome.options import Options
import re

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
        self.driver = webdriver.Chrome(options=chrome_options)
        self.url = 'https://uk.webuy.com/search?stext=iphone%207%20plus'
        self.phones_names_list = []
        self.phones_price_list = []
        self.url_list = []
        self.spec_list = []
        self.price_list = []

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
    
    def get_all_phone_url(self):
        # previous_url = ''
        # while (True):
        #     if self.driver.current_url != previous_url:
        #         print(previous_url)
        #         previous_url = self.driver.current_url
        #         self.append_all_url_to_list()
        #         next_page = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Next"]')
        #         next_page.click()
        #         print(self.driver.current_url)
        #         time.sleep(2)
        #     else:
        #         print('HERE')
        #         break

        self.append_all_url_to_list()
        next_page = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Next"]')
        next_page.click()
        time.sleep(2)
    
    def append_all_url_to_list(self):
        parent = self.driver.find_elements(By.CSS_SELECTOR, value='a.line-clamp')
        for i in parent:
            self.url_list.append(i.get_attribute('href'))
    
    def go_into_page_and_out(self):
        """
        The option that allows access to the image class is only made available after going into
        a device link and coming back out.
        """
        
        for url in self.url_list:
            self.driver.execute_script("window.open('');") 
            self.driver.switch_to.window(self.driver.window_handles[1]) 
            self.driver.get(url)
            time.sleep(10)
            self.product_prices()
            self.product_spec()
            time.sleep(5)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(5)
        print('DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    def product_spec(self):
        self.spec_list = []
        product_detail = self.driver.find_elements(By.CSS_SELECTOR, 'span[class="text-sm"]')
        for i in product_detail:
            self.spec_list.append(i.text)
        self.phone_name_and_condition()
    
    def product_prices(self):
        self.price_list = []
        prices = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="d-flex flex-wrap w-100"]')
        for i in prices:
            price = i.text
            self.price_list.append(price)
        self.price_list = re.findall(r'\d+\.\d+', self.price_list[0])
        self.price_list = [float(num) for num in self.price_list]


    
    def phone_name_and_condition(self):
        """
        Find all span tags and classes that correlate with the desired device names.
        """
        dict_phones = {'Manufacturer': [], 'Phone Model': [], 'Network': [], 'Grade': [], 'Capacity': [], 'Phone Colour': [], 'Main Colour': [], 'OS': [], 'Physical SIM Slots': [], 'Price': [], 'Trade-in for Voucher': [], 'Trade-in for cash': []}
        dict_phones['Manufacturer'].append(self.spec_list[0])
        dict_phones['Phone Model'].append(self.spec_list[1])
        dict_phones['Network'].append(self.spec_list[2])
        dict_phones['Grade'].append(self.spec_list[3])
        dict_phones['Capacity'].append(self.spec_list[4])
        dict_phones['Phone Colour'].append(self.spec_list[5])
        dict_phones['Main Colour'].append(self.spec_list[6])
        dict_phones['OS'].append(self.spec_list[7])
        dict_phones['Physical SIM Slots'].append(self.spec_list[8])
        dict_phones['Price'].append(self.price_list[0])
        dict_phones['Trade-in for Voucher'].append(self.price_list[1])
        dict_phones['Trade-in for cash'].append(self.price_list[2])
        self.phones_names_list.append(dict_phones)

        

if __name__ == '__main__':
    start_crawling = Crawler()
    start_crawling.load_and_accept_cookies()
    start_crawling.select_iphone()
    start_crawling.get_all_phone_url()
    start_crawling.go_into_page_and_out()
