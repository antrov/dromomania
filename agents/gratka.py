from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from enum import Enum
from urllib.parse import urlparse
from urllib.parse import parse_qs

QS_PAGE_KEY = 'page'

class Browser(Enum):
    BRAVE = 1
    FIREFOX = 2

def get_driver_brave():
    options = ChromeOptions()
    options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    # options.add_argument("--headless")
    return webdriver.Chrome(options = options)

def get_driver_firefox():
    options = FirefoxOptions()
    # options.add_argument("--headless")
    return webdriver.Firefox(options=options)


def get_driver(browser: Browser):
    match browser:
        case Browser.BRAVE:
            return get_driver_brave()
        case Browser.FIREFOX:
            return get_driver_firefox()

driver = get_driver(Browser.FIREFOX)

def scrap(page: int):
    driver.get(f'https://gratka.pl/nieruchomosci/morgi-30504?promien=5&{QS_PAGE_KEY}={page}')
    if driver.find_elements(By.CSS_SELECTOR, ".errorPage__title"):
        return False

    # scrap
    for my_elem in WebDriverWait(driver, 60).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.listing__teaserWrapper"))):
        try:
            href = my_elem.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            title = my_elem.find_element(By.CSS_SELECTOR, ".teaserUnified__title").get_attribute("innerText")
            src = my_elem.find_element(By.CSS_SELECTOR, "img.teaserUnified__img").get_attribute("src")
            params = my_elem.find_element(By.CSS_SELECTOR, ".teaserUnified__params").get_attribute("innerText")
            print(f'{title} {params} - {href} -  {src}')
        except NoSuchElementException as ex:
            print(ex.msg)

    return True

page = 1
while scrap(page):
    page += 1   
    
driver.close()