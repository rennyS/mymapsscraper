from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class GoogleEarthAutomation:
    def __init__(self, geckodriver_path, custom_profile_path, firefox_binary_path):
        """
        Initialise the GoogleEarthAutomation class

        Arguments:
            geckodriver_path (str): Path to the geckodriver executable
            custom_profile_path (str): Path to the custom Firefox profile to use
            firefox_binary_path (str): Path to the Firefox binary executable
        """
        self.geckodriver_path = geckodriver_path
        self.custom_profile_path = custom_profile_path
        self.firefox_binary_path = firefox_binary_path
        self.driver = self.setup_driver()

    def setup_driver(self):
        """
        Setup the webdriver instance to be used for automation

        Returns:
            webdriver.Firefox: A headless Firefox webdriver instance
        """
        options = Options()
        # Set the browser to run in headless mode
        options.headless = True
        # Set the path to the Firefox binary
        options.binary_location = self.firefox_binary_path
        # Set the custom profile to be used
        options.profile = self.custom_profile_path

        # Set the path to the geckodriver executable
        service = Service(self.geckodriver_path)
        # Create a new Firefox webdriver instance
        driver = webdriver.Firefox(options=options, service=service)
        return driver

    def run_google_earth_automation(self):
        self.driver.get('https://www.google.com/maps/d/viewer?mid=1U51M8KYT6NgT8TNrfUCPxRGRgj-deZU&ll=54.17131499483824%2C-1.2018284499999936&z=4')
        time.sleep(4)

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
        time.sleep(3)
        webdriver.ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('e').key_up(Keys.CONTROL).perform()

    def close_driver(self):
        time.sleep(1)
        self.driver.quit()

# Set the paths
geckodriver_path = 'geckodriver.exe'
custom_profile_path = r"webdriverprofile_folder"
firefox_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'

# Create an instance of the GoogleEarthAutomation class
google_earth_automation = GoogleEarthAutomation(geckodriver_path, custom_profile_path, firefox_binary_path)
google_earth_automation.run_google_earth_automation()
google_earth_automation.close_driver()
