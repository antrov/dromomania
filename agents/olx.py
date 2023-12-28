from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from agents import QS_DEFAULT_PAGE_KEY, ScrapAgent, ScrappedOffer


class OlxAgent(ScrapAgent):
    def scrap_item(self, my_elem: WebElement) -> ScrappedOffer|None:
        try:
            href = my_elem.get_attribute("href")
            img = my_elem.find_element(By.CSS_SELECTOR, "img")
            title = img.get_attribute("alt")
            src = img.get_attribute("src")
            params = my_elem.find_element(By.CSS_SELECTOR, "div[color=text-global-secondary] span").get_attribute("innerText")  
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

        if page > 1 and not self.url_is_on_page(self.driver.current_url, page):
            return False

        self.wait_page_ready()
        self.scroll_to_bottom(2)

        offers = []
        for e in self.wait_for_elements("div[data-cy=l-card] a"):
            offers.append(self.scrap_item(e))
        return offers


OlxAgent(
    url = 'https://www.olx.pl/nieruchomosci/dzialki/ldzan/?search%5Bdist%5D=15&view=grid',
    tag = 'latyfundia',
).scrap()