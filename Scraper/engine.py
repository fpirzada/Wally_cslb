import random
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import traceback

# The SeleniumBrowserManager class is designed to create and manage Selenium browser instances.
# It includes several methods to set up browser configuration, such as user agents, proxies, and caching.
# It also provides methods for managing browser instances, such as opening and closing browsers.
class Engine:
        
    def __init__(self):
        os.environ["SSL_CERT_FILE"] = "/Users/mac/Documents/BOT/Auto-Job-Apply/venv/lib/python3.10/site-packages/certifi/cacert.pem"
 
    def create_browser(self, timeout: int = 5, headless: bool = True, proxy: str = None, window_size: str = 'start-maximized', clear_cache: bool = False):
        try:
            # Main function to create and configure a browser instance  
            chrome_options = webdriver.ChromeOptions()
            chrome_options = self._configure_chrome_options(chrome_options, window_size, headless)
            # self._configure_user_agents(chrome_options)
            self._configure_cache(clear_cache)

            # # Set desired capabilities
            # desired_capabilities = DesiredCapabilities.CHROME.copy()
            # desired_capabilities['goog:chromeOptions'] = {'debuggerAddress': '127.0.0.1:9222'}

            # Create the WebDriver instance
            browser = webdriver.Chrome(options=chrome_options)

            # Maximize the browser window (full screen)
            browser.maximize_window()
            browser_version = browser.capabilities['browserVersion']
            driver_version = browser.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
            print("browser version", browser_version)
            print("driver version", driver_version)
            self._configure_default_timeout(browser, timeout)
            self._clear_browser_cache(clear_cache, browser)

            return browser
        except Exception as e:
            print(e)

    def _configure_chrome_options(self, chrome_options, window_size, headless):
       
        # Other options to enhance compatibility and bypass detection
        # chrome_options.add_argument("--lang=en-us")
        # chrome_options.add_argument("--disable-web-security")
        # chrome_options.add_argument("--allow-running-insecure-content")
        # chrome_options.add_argument("--ignore-certificate-errors")
        
        # Enable headless mode if specified
        if headless:
            chrome_options.add_argument("--headless")
        
        # Disable GPU acceleration and other browser extensions
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        
        # Disable various Chrome features that might trigger detection
        # chrome_options.add_argument("--disable-popup-blocking")
        # chrome_options.add_argument("--disable-plugins-discovery")
        # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Disable browser-side navigation
        # chrome_options.add_argument("--disable-browser-side-navigation")

        # Set the window size for the browser
        chrome_options.add_argument(window_size)
        
        return chrome_options
   
    @staticmethod
    def _configure_default_timeout(browser: webdriver.Chrome, timeout: int):
        # Configures the default timeouts for the browser instance
        SECONDS = 60
        timeout = timeout * SECONDS
            
        browser.set_page_load_timeout(timeout)
        browser.implicitly_wait(timeout)
        
    @staticmethod
    def _configure_cache(clear_cache: bool):
        # Configures the cache settings for the browser instance
        if clear_cache:
            # Disables the application cache to prevent storing web application data.
            chrome_options.add_argument('--disable-application-cache')

            # Sets the disk cache size to 0 bytes, effectively disabling the disk cache.
            chrome_options.add_argument('--disk-cache-size=0')

            # Creates a dictionary with 'disk-cache-size' set to 0.
            prefs = {'disk-cache-size': 0}

            # This also sets the disk cache size to 0, disabling the disk cache.
            chrome_options.add_experimental_option('prefs', prefs)

    @staticmethod
    def _clear_browser_cache(clear_cache: bool, browser: webdriver.Chrome):
        # Clears the browser cache if clear_cache is set to True
        if clear_cache:
            # Executes a Chrome DevTools Protocol command to disable the cache.
            # This command disables caching of all resources for the lifetime of the browser.
            browser.execute_cdp_cmd('Network.setCacheDisabled', {'cacheDisabled': True})

            # Deletes all cookies stored by the browser.
            browser.delete_all_cookies()
    
    @staticmethod
    def close_selenium_browser(browser: webdriver.Chrome):
        # Closes the browser instance and handles any exceptions
        try:
            browser.quit()
        except Exception as e:
            traceback.print_exc()
    