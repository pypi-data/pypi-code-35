from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from platform import system
from time import sleep
import os
from subprocess import call
from csv import reader
from random import choice


class SeleniumBot:
    def __init__(self):
        self.loading_time = 1
        self.driver = self.__get_driver()

    def __get_driver(self):
        driverPath = self.__get_driver_Path(system())
        driver_options = self.__get_driver_options()
        driver = webdriver.Chrome(driverPath, options=driver_options)
        return driver

    def __get_driver_Path(self, operating_system):
        cwd = os.path.dirname(__file__)
        if operating_system == "Windows":
            chrome_driver_path = f"{cwd}/webdrivers/chromedriverWindows.exe"
            return chrome_driver_path
        elif operating_system == "MacOS":
            chrome_driver_path = f"{cwd}/webdrivers/chromedriverMac"
            return chrome_driver_path
        else:
            chrome_driver_path = f"{cwd}/webdrivers/chromedriverLinux"
            call(["chmod", "+x", chrome_driver_path])
            return chrome_driver_path
    
    def __get_driver_options(self):
        user_agent = self.__get_random_user_agent()
        options = Options()
        options.add_argument(f"User-Agent={user_agent}")
        return options
    
    def __get_random_user_agent(self):
        cwd = os.path.dirname(__file__)
        with open("{cwd}/webdrivers/user_agents.csv") as user_agents_file:
            reader = reader(user_agents_file)
            chosen_user_agent = choice(list(reader))
            return chosen_user_agent
        

    def go_to_page(self, url):
        self.driver.get(url)

    def post_click_or_submit(self, element):
        try:
            element.click()
        except:
            element.submit()

    def get_element_text(self, element):
        return element.text

    def post_text_to_element(self, element, text):
        element.send_keys(text)

    def get_element_by_css_selector(self, css_selector):
        try:
            waiting = WebDriverWait(
                driver=self.driver, timeout=self.loading_time * 8
            )
            element_to_wait = waiting.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return element_to_wait
        except:
            return None

    def get_elements_by_css_selector(self, css_selector):
        try:
            return self.driver.find_elements_by_css_selector(css_selector)
        except:
            return None
