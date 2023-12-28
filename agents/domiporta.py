from urllib.parse import parse_qs, urlparse
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
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


class ScrapAgent:
    def get_driver_brave(self):
        options = ChromeOptions()
        options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
        # options.add_argument("--headless")
        return webdriver.Chrome(options=options)

    def get_driver_firefox(self):
        options = FirefoxOptions()
        # options.add_argument("--headless")
        return webdriver.Firefox(options=options)

    def get_driver(self, browser: Browser):
        match browser:
            case Browser.BRAVE:
                return self.get_driver_brave()
            case Browser.FIREFOX:
                return self.get_driver_firefox()

    def scroll_to_bottom(self, driver: RemoteWebDriver, step: int = 2):
        total_height = driver.execute_script(
            "return document.documentElement.scrollHeight")
        for i in range(1, total_height, 1):
            driver.execute_script("window.scrollTo(0, {});".format(i))

    def url_is_on_page(self, url: str, page_key: str, expected_page: int) -> bool:
        parsed_url = urlparse(url)
        qs = parse_qs(parsed_url.query)
        if page_key not in qs:
            print(f'No page key in url {qs}')
            return False
        if not qs[page_key]:
            print('Page index is empty')
            return False
        page_index = qs[page_key][0]
        if page_index != str(expected_page):
            print(
                f'Page index {page_index} not match expected {expected_page}')
            return False
        return True

    def wait_page_ready(self, driver: RemoteWebDriver):
        WebDriverWait(driver, 10).until(lambda driver:
                                        driver.execute_script(
                                            'return document.readyState') == 'complete'
                                        )

    def wait_for_elements(self, driver: RemoteWebDriver, css_selector: str) -> [WebElement]:
        return WebDriverWait(driver, 60).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector)))

    def scrap_page(self, driver: RemoteWebDriver, url: str, page: int) -> bool:
        return False

    def scrap(self):
        driver = self.get_driver(Browser.FIREFOX)
        url = 'https://www.domiporta.pl/nieruchomosci/sprzedam/lodzkie/kolonia-ldzan?Distance=5'
        page = 1
        while self.scrap_page(driver, url, page):
            page += 1

        driver.close()


class DomiportaAgent(ScrapAgent):
    def scrap_page(self, driver: RemoteWebDriver, url: str, page: int) -> bool:
        driver.get(f'{url}&{QS_PAGE_KEY}={page}')

        if page > 1 and not self.url_is_on_page(driver.current_url, QS_PAGE_KEY, page):
            return False

        self.wait_page_ready(driver)
        self.scroll_to_bottom(driver, 1)

        # scrap
        for my_elem in self.wait_for_elements(driver, "article.sneakpeak"):
            try:
                pic_container = my_elem.find_element(
                    By.CSS_SELECTOR, "a.sneakpeak__picture_container")
                href = pic_container.get_attribute("href")
                title = pic_container.get_attribute("title")
                src = pic_container.find_element(
                    By.CSS_SELECTOR, "img.loaded").get_attribute("src")
                param_items = []
                for param_element in my_elem.find_elements(By.CSS_SELECTOR, "span.sneakpeak__details_item"):
                    param = param_element.text.replace("\n", "").strip()
                    if param:
                        param_items.append(param)
                params = ' - '.join(param_items)
                print(f'{title} {params} - {href} -  {src}')
            except NoSuchElementException as ex:
                print(ex.msg)


DomiportaAgent().scrap()
