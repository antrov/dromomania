from urllib.parse import parse_qs, urlparse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from enum import Enum

QS_PAGE_KEY = 'PageNumber'

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
    driver.get(f'https://www.domiporta.pl/nieruchomosci/sprzedam/lodzkie/kolonia-ldzan?Distance=5&{QS_PAGE_KEY}={page}')
    parsed_url = urlparse(driver.current_url)
    qs = parse_qs(parsed_url.query)
    if page > 1:
        if QS_PAGE_KEY not in qs:
            print(f'No page key in url {qs}')
            return False
        if not qs[QS_PAGE_KEY]:            
            print('Page index is empty')
            return False
        page_index = qs[QS_PAGE_KEY][0]
        if page_index != str(page):
            print(f'Page index {page_index} not match requested {page}')
            return False

    total_height = driver.execute_script("return document.documentElement.scrollHeight")
    for i in range(1, total_height, 2):
        driver.execute_script("window.scrollTo(0, {});".format(i))

    # scrap
    for my_elem in WebDriverWait(driver, 60).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "article.sneakpeak"))):
        try:
            pic_container = my_elem.find_element(By.CSS_SELECTOR, "a.sneakpeak__picture_container")
            href = pic_container.get_attribute("href")
            title = pic_container.get_attribute("title")
            src = pic_container.find_element(By.CSS_SELECTOR, "img.loaded").get_attribute("src")
            params = my_elem.find_element(By.CSS_SELECTOR, "div.sneakpeak__details").get_attribute("innerText")
            print(f'{title} {params} - {href} -  {src}')
        except NoSuchElementException as ex:
            print(ex.msg)

    return True

page = 1
while scrap(page):
    page += 1   
    
driver.close()