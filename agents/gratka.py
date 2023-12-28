from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from agents import QS_DEFAULT_PAGE_KEY, ScrapAgent, ScrappedOffer


class GratkaAgent(ScrapAgent):
    def scrap_item(self, my_elem: WebElement) -> ScrappedOffer|None:
        try:
            href = my_elem.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            title = my_elem.find_element(By.CSS_SELECTOR, ".teaserUnified__title").get_attribute("innerText")
            src = my_elem.find_element(By.CSS_SELECTOR, "img.teaserUnified__img").get_attribute("src")
            params = my_elem.find_element(By.CSS_SELECTOR, ".teaserUnified__params").get_attribute("innerText")      
            return ScrappedOffer(
                image_url = src,
                offer_url = href,
                title = title,
                params = params,
                tag = self.tag
            )
        except NoSuchElementException as ex:
            print(ex.msg)

    def scrap_page(self, page: int) -> bool|list:
        self.driver.get(f'{self.url}&{QS_DEFAULT_PAGE_KEY}={page}')

        if self.driver.find_elements(By.CSS_SELECTOR, ".errorPage__title"):
            return False

        self.wait_page_ready()

        offers = []
        for e in self.wait_for_elements("div.listing__teaserWrapper"):
            offers.append(self.scrap_item(e))
        return offers


GratkaAgent(
    url = 'https://gratka.pl/nieruchomosci/morgi-30504?promien=5',
    tag = 'latyfundia',
).scrap()