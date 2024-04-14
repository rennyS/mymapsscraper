from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import os

class GoogleEarthAutomation:
    def __init__(self, geckodriver_path, custom_profile_path, firefox_binary_path):
        self.geckodriver_path = geckodriver_path
        self.custom_profile_path = custom_profile_path
        self.firefox_binary_path = firefox_binary_path
        self.driver = self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.headless = True
        options.binary_location = self.firefox_binary_path
        options.profile = self.custom_profile_path

        service = Service(self.geckodriver_path)
        driver = webdriver.Firefox(options=options, service=service)
        return driver

    def run_google_earth_automation(self):
        self.driver.get('MAPS_URL_HERE')
        time.sleep(4)
        with open('local_storage_data.json', 'r') as file:
            updated_value = file.read()

        container_div = self.driver.find_element(By.CSS_SELECTOR, "div.mU4ghb-xl07Ob-LgbsSe[jscontroller='GC9WS']")
        container_div.click()
        time.sleep(2)

        view_earth_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='View map in Google Earth']")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", view_earth_button)

        main_tab_handle = self.driver.current_window_handle
        view_earth_button.click()
        time.sleep(1)
        tab_handles = self.driver.window_handles
        new_tab_handle = [handle for handle in tab_handles if handle != main_tab_handle][0]
        self.driver.switch_to.window(new_tab_handle)
        js_code = """
        window.localStorage.setItem('earth.HasSeenOnboardingDialog', 'true');
        """
        self.driver.execute_script(js_code)

        with open('cookies.json', 'r') as file:
            cookies = json.load(file)
        for cookie in cookies:
            self.driver.add_cookie(cookie)

        new_page_url = self.driver.current_url
        time.sleep(2)
        cookies = self.driver.get_cookies()
        time.sleep(1)
        webdriver.ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('e').key_up(Keys.CONTROL).perform()

    def close_driver(self):
        self.driver.quit()

# Set the paths
geckodriver_path = 'geckodriver.exe'
custom_profile_path = r"C:\Users\laure\Documents\VSCode\webdriverprofile"
firefox_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'

# Create an instance of the GoogleEarthAutomation class
google_earth_automation = GoogleEarthAutomation(geckodriver_path, custom_profile_path, firefox_binary_path)
google_earth_automation.run_google_earth_automation()
google_earth_automation.close_driver()
