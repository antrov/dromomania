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
    driver.get(f'https://www.olx.pl/nieruchomosci/dzialki/ldzan/?{QS_PAGE_KEY}={page}&search%5Bdist%5D=15&view=grid')
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
    # driver.get("https://www.olx.pl/nieruchomosci/ldzan/?search%5Bdist%5D=50&view=grid")
        
    # dismiss cookies popup
    # try:
    #     cookies_button = (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler")
    #     WebDriverWait(driver, 5).until(EC.element_to_be_clickable(cookies_button)).click()
    #     WebDriverWait(driver, 5).until(EC.invisibility_of_element_located(cookies_button))
    # except TimeoutException:
    #     print()

    # scroll to load
    total_height = driver.execute_script("return document.documentElement.scrollHeight")
    for i in range(1, total_height, 2):
        driver.execute_script("window.scrollTo(0, {});".format(i))

    # scrap
    for my_elem in WebDriverWait(driver, 60).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[data-cy=l-card] a"))):
        try:
            href = my_elem.get_attribute("href")
            img = my_elem.find_element(By.CSS_SELECTOR, "img")
            title = img.get_attribute("alt")
            src = img.get_attribute("src")
            params = my_elem.find_element(By.CSS_SELECTOR, "div[color=text-global-secondary] span").get_attribute("innerText")  
            # urllib.request.urlretrieve(src, filename=f'samples/olx_{uuid.uuid4().hex[:6]}.webp')
            print(f'{title} {params} - {href}')
        except NoSuchElementException as ex:
            print(ex.msg)

    return True

# driver.save_screenshot('screenie.png')
page = 1
while scrap(page):
    page += 1   
    
driver.close()  