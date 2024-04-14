# Google Earth Automation with Selenium

Automate downloading of KML by navigating to google earth page from google mymaps url.

## Description

This project provides a Python script that automates interactions with Google Maps and Google Earth using the Selenium WebDriver. The script navigates to a specific Google Maps link, commands it to use a specific hotkey, and then downloads the KML file for later use.

## Features

- Headless browsing with Firefox
- Clicking on elements and scrolling to view
- Setting local storage data
- Adding cookies
- Simulating keyboard shortcuts

## Installation

1. Clone the repository:

2. git clone https://github.com/rennyS/mymapsscraper.git

2. Install the required dependencies:
```pip install selenium```

3. Download the geckodriver executable for Firefox and set the paths in the script.

## Usage

1. Update the paths for `geckodriver`, ```custom Firefox profile```, and ```Firefox binary``` in the script, to your geckodriver file location, custom firefox profile location and your firefox binary (typically default firefox.exe location)
2. Run the `main.py` script to start the automation process: ```python main.py```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Selenium WebDriver: https://www.selenium.dev/documentation/en/webdriver/
- Mozilla Firefox: https://www.mozilla.org/en-US/firefox/

Feel free to customize this template with specific details about your project and any additional information you would like to include.
You can copy and paste this content into a file named README.md in the root directory of your project, and it will be the README file structure for your GitHub repository.


