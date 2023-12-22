from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request
import uuid

# setup
options = Options()
options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
# options.add_argument("--headless")
driver = webdriver.Chrome(options = options)
# driver.get("https://www.olx.pl/nieruchomosci/ldzan/?search%5Bdist%5D=50&view=grid")
driver.get("https://www.olx.pl/nieruchomosci/dzialki/ldzan/?search%5Bdist%5D=5&view=grid")

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
        alt = img.get_attribute("alt")
        src = img.get_attribute("src")
        # urllib.request.urlretrieve(src, filename=f'samples/olx_{uuid.uuid4().hex[:6]}.webp')
        print(f'{alt} - {href}')
    except NoSuchElementException as ex:
        print(ex.msg)

# driver.save_screenshot('screenie.png')

driver.close()