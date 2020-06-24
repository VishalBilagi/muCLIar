import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


def create_driver():
    """
    Create a webdriver instance of Firefox
    :return: Friefox driver instance
    """

    options = Options()

    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Firefox(options=options)
    extention_path = os.path.dirname(os.path.abspath(__file__))+"/ghostery_privacy_ad_blocker-8.5.1-an+fx.xpi"
    driver.install_addon(extention_path, temporary=True)

    return driver
