from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from agents import ScrapAgent, ScrappedOffer

QS_PAGE_KEY = 'PageNumber'

class DomiportaAgent(ScrapAgent):
    def scrap_item(self, my_elem: WebElement) -> ScrappedOffer|None:
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
        self.driver.get(f'{self.url}&{QS_PAGE_KEY}={page}')

        if page > 1 and not self.url_is_on_page(self.driver.current_url, QS_PAGE_KEY, page):
            return False

        self.wait_page_ready()
        self.scroll_to_bottom(10)

        offers = []
        for e in self.wait_for_elements("article.sneakpeak"):
            offers.append(self.scrap_item(e))
        return offers


DomiportaAgent(
    url = 'https://www.domiporta.pl/nieruchomosci/sprzedam/lodzkie/kolonia-ldzan?Distance=5',
    tag = 'latyfundia',
).scrap()
