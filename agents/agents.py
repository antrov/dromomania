from enum import Enum
from urllib.parse import parse_qs, urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

QS_DEFAULT_PAGE_KEY = "page"


class Browser(Enum):
    BRAVE = 1
    FIREFOX = 2


class ScrappedOffer:
    def __init__(self, image_url: str, offer_url: str, title: str, params: str | None, tag: str):
        self.image_url = image_url
        self.offer_url = offer_url
        self.title = title
        self.params = params
        self.tag = tag

    def __str__(self):
        return ' - '.join([self.title, self.params, f'#{self.tag}', self.offer_url])


class ScrapAgent:
    def __init__(self, url: str, tag: str, browser: Browser = Browser.FIREFOX):
        self.url = url
        self.tag = tag
        self.driver = self.get_driver(browser)

    def get_driver_brave(self):
        options = ChromeOptions()
        options.binary_location = (
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        )
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

    def scroll_to_bottom(self, step: int = 2):
        total_height = self.driver.execute_script(
            "return document.documentElement.scrollHeight"
        )
        for i in range(1, total_height, 1):
            self.driver.execute_script("window.scrollTo(0, {});".format(i))

    def url_is_on_page(
        self, url: str, expected_page: int, page_key: str = QS_DEFAULT_PAGE_KEY
    ) -> bool:
        parsed_url = urlparse(url)
        qs = parse_qs(parsed_url.query)
        if page_key not in qs:
            print(f"No page key in url {qs}")
            return False
        if not qs[page_key]:
            print("Page index is empty")
            return False
        page_index = qs[page_key][0]
        if page_index != str(expected_page):
            print(f"Page index {page_index} not match expected {expected_page}")
            return False
        return True

    def wait_page_ready(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )

    def wait_for_elements(self, css_selector: str) -> list[WebElement]:
        return WebDriverWait(self.driver, 60).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector))
        )

    def scrap_page(self, page: int) -> bool | list:
        return False

    def scrap(self):
        page = 1
        offers = []
        while True:
            os = self.scrap_page(page)
            if isinstance(os, list):
                _ = [print(o) for o in list(os)]
            if not os:
                break
            offers.append(os)
            page += 1

        self.driver.close()
