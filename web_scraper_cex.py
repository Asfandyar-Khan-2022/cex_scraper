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
        self.url = 'https://uk.webuy.com/search/?stext=iphone%207%20plus'
        self.phones_names_list = []
        self.phones_price_list = []
        self.image_url_list = []


    def load_and_accept_cookies(self) -> webdriver.Chrome:
        """
        Accept the cookies prompt.
        """
        self.url = 'https://uk.webuy.com/search/?stext=iphone%207%20plus'
        self.driver.get(self.url)
        time.sleep(3)
        accept_cookies_button = self.driver.find_element(By.XPATH,
        value='//*[@id="onetrust-accept-btn-handler"]')
        accept_cookies_button.click()
        time.sleep(1)


    def device_grade(self):
        """
        Find the tick box responsible for grade a and click on it to only show grade a results.
        Do the same for grade b.
        """
        grade_a = self.driver.find_element(By.XPATH,
        value='//*[@id="main"]/div/div/div[1]/div[2]/div/div[3]/div[1]/div/div[3]/div[46]/div/div/div/ul/li[2]/label/span[1]')
        grade_a.click()
        time.sleep(1)
        grade_b = self.driver.find_element(By.XPATH,
        value='//*[@id="main"]/div/div/div[1]/div[2]/div/div[3]/div[1]/div/div[3]/div[46]/div/div/div/ul/li[1]/label/span[1]')
        grade_b.click()


    def go_into_page_and_out(self):
        """
        The option that allows access to the image class is only made available after going into
        a device link and coming back out.
        """
        in_and_out = self.driver.find_element(By.XPATH,
        value ='//*[@id="__layout"]/div/div[6]/div[1]/div[2]/'\
                'div/div/div/div/div[3]/div[1]/div/div[2]/h1/a/span')
        in_and_out.click()
        time.sleep(3)
        self.driver.back()
        time.sleep(3)


    def scroll_to_bottom(self):
        """
        The page scrolls to the bottom so that all device names are made available.
        As otherwise not all the data can be collected.

        Return:
            Return true when the bottom of the page has been reached
        """
        previouse_height = self.driver.execute_script('return document.body.scrollHeight')

        while True:
            self.driver.execute_script('window.scrollTo(0,document.body.clientHeight)')
            time.sleep(3)
            new_height = self.driver.execute_script('return document.body.scrollHeight')

            if new_height == previouse_height:
                break
            previouse_height = new_height

        return True


    def gather_image_data(self):
        """
        Find all img tags and classes that correlate with the desired images.
        Save the URL links in a list
        """
        image_data = self.driver.find_elements(By.CSS_SELECTOR, 'img.t058-product-img')

        for i in image_data:
            dict_image_link = {}
            dict_image_link['Image url'] = [i.get_attribute('src')]
            self.image_url_list.append(dict_image_link)


    def buying_and_selling_price(self):
        """
        Group the selling and buying data for each device.
        As in its current state the data is all split in a list.
        """
        new_list = []
        we_sell_price = self.driver.find_elements(By.CSS_SELECTOR, 'div.priceTxt')
        for i in we_sell_price:
            new_list.append(i.text)
        composite_list = [new_list[x:x+3] for x in range(0, len(new_list),3)]

        for i in composite_list:
            dict_phones_price = {}
            dict_phones_price['Price'] = i
            self.phones_price_list.append(dict_phones_price)


    def phone_name_and_condition(self):
        """
        Find all span tags and classes that correlate with the desired device names.
        """
        phone_name = self.driver.find_elements(By.CSS_SELECTOR, 'span.ais-Highlight')
        for i in phone_name:
            dict_phones = {'Phone': [], 'Condition': [], 'Price': [], 'Image url': [], 'Time': []}
            dict_phones['Phone'].append(i.text)
            dict_phones['Condition'].append(i.text[-1])
            self.phones_names_list.append(dict_phones)


    def add_url_price_time_to_dictionary(self):
        """
        Add the price data and the current time to the dictionary.
        """
        for i, _ in enumerate(self.phones_names_list):
            self.phones_names_list[i]['Price'] = self.phones_price_list[i]['Price']
            self.phones_names_list[i]['Image url'] = self.image_url_list[i]['Image url']
            now = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
            self.phones_names_list[i]['Time'] = now


    def download_img(self):
        """
        Download all the images and store them locally in the current directory.
        """
        for i, _ in enumerate(self.image_url_list):
            image_url = self.image_url_list[i]['Image url'][0]
            now = str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
            filename = f'{now}_{str(i)}.jpg'
            connect_to_img_url = requests.get(image_url, stream = True, timeout=5)

            if connect_to_img_url.status_code == 200:
                connect_to_img_url.raw.decode_content = True

                with open(filename,'wb') as file:
                    shutil.copyfileobj(connect_to_img_url.raw, file)

                print('Image sucessfully Downloaded: ',filename)
            else:
                print('Image Couldn\'t be retrieved')

if __name__ == '__main__':
    start_crawling = Crawler()
    start_crawling.load_and_accept_cookies()
    start_crawling.device_grade()
    start_crawling.go_into_page_and_out()
    if start_crawling.scroll_to_bottom():
        start_crawling.gather_image_data()
        start_crawling.buying_and_selling_price()
        start_crawling.phone_name_and_condition()
        start_crawling.add_url_price_time_to_dictionary()
        start_crawling.download_img()
    start_crawling.driver.quit()