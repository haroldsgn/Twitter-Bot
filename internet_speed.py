import os
import time

import selenium
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

PROMISED_MB = 300
CHROME_DRIVER_PATH = "C:\development\chromedriver-win64\chromedriver.exe"
TWITTER_EMAIL = os.environ.get("EMAIL")
TWITTER_PASSWORD = os.environ.get("PASSWORD")
PHONE_NUMBER = "3142261859"


class InternetSpeedTwitterBot:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)
        self.service = Service(executable_path=CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")

        go_button = self.driver.find_element(By.CSS_SELECTOR, '.start-button a')
        go_button.click()

        time.sleep(50)
        down_mb = self.driver.find_element(By.XPATH,
                                           '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div['
                                           '3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
        self.down = float(down_mb)
        up_mb = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div['
                                                   '3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
        self.up = float(up_mb)
        return self.up, self.down

    def tweet_at_provider(self):

        self.driver.get("https://twitter.com/i/flow/login?redirect_after_login=%2F")
        self.driver.maximize_window()

        time.sleep(10)
        email = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                   '2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div['
                                                   '2]/div/input')
        email.send_keys(TWITTER_EMAIL)
        submit_email = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                          '2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
        submit_email.click()

        time.sleep(5)

        try:
            phone_number = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                              '2]/div/div/div[2]/div[2]/div[1]/div/div['
                                                              '2]/label/div/div[2]/div')
            phone_number.find_element(By.TAG_NAME, 'input').send_keys(PHONE_NUMBER)
            submit_phone_number = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div['
                                                                     '1]/div/div/div/div/div/div/div[2]/div['
                                                                     '2]/div/div/div[2]/div[2]/div['
                                                                     '2]/div/div/div/div/div')
            submit_phone_number.click()
        except NoSuchElementException:
            print("There are not security steps.")
            pass

        time.sleep(3)
        password = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                      '2]/div/div/div[2]/div[2]/div[1]/div/div/div['
                                                      '3]/div/label/div/div[2]/div[1]')
        password.find_element(By.TAG_NAME, "input").send_keys(TWITTER_PASSWORD)
        submit_password = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                             '2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')
        submit_password.click()

        time.sleep(20)

#         Writing the tweet
        tweet_box = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div['
                                                       '2]/main/div/div/div/div/div/div[3]/div/div[2]/div['
                                                       '1]/div/div/div/div[2]/div['
                                                       '1]/div/div/div/div/div/div/div/div/div/div/label/div['
                                                       '1]/div/div/div/div/div/div[2]/div/div/div/div')
        tweet_box.click()
        time.sleep(2)
        w_tweet = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div['
                                                     '2]/main/div/div/div/div/div/div[3]/div/div[2]/div['
                                                     '1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div['
                                                     '2]/div/div/div/div/label/div[1]/div/div/div/div/div/div['
                                                     '2]/div/div/div/div/span/br')
        w_tweet.send_keys(f"Hola @ClaroTeAyuda, por que mi velocidad de internet es {self.down}down/{self.up}up "
                          f"cuando pagué por {PROMISED_MB}mb?")
        time.sleep(3)
        submit_tweet = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div['
                                                          '2]/main/div/div/div/div/div/div[3]/div/div[2]/div['
                                                          '1]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div['
                                                          '3]/div')
        submit_tweet.click()
