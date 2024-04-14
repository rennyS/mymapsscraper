from scrapemapsforearth import GoogleEarthAutomation


geckodriver_path = 'geckodriver.exe'
custom_profile_path = r"CUSTOM/FIREFOX/PROFILE/FOLDER"
firefox_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'

GoogleEarthAutomation = GoogleEarthAutomation(geckodriver_path, custom_profile_path, firefox_binary_path)

# Create an instance of the GoogleEarthAutomation class
google_earth_automation = GoogleEarthAutomation(geckodriver_path, custom_profile_path, firefox_binary_path)
google_earth_automation.run_google_earth_automation()

google_earth_automation.close_driver()
