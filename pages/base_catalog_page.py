from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from framework.base_page import BasePage
from framework.models import ProductCard
from framework.utils import normalize_space, parse_money


class BaseCatalogPage(BasePage):
    SORT_DROPDOWN = (By.CSS_SELECTOR, "select[name='sort']")
    PRODUCT_NAME_LINKS = (By.CSS_SELECTOR, ".thumbnails .fixed_wrapper .prdocutname")

    def sort_by_visible_text(self, value: str):
        current_marker = self.get_product_link_elements()[0]
        Select(self.find(self.SORT_DROPDOWN)).select_by_visible_text(value)
        self.waits.staleness(current_marker)
        self.wait_until_ready()
        return self

    def get_product_link_elements(self):
        return [element for element in self.find_all(self.PRODUCT_NAME_LINKS) if element.text.strip()]

    def get_products(self) -> list[ProductCard]:
        products: list[ProductCard] = []
        for link in self.get_product_link_elements():
            card = link.find_element(By.XPATH, "./ancestor::div[contains(@class,'col-md-3')]")
            products.append(
                ProductCard(
                    name=normalize_space(link.text),
                    price=parse_money(card.find_element(By.CSS_SELECTOR, ".oneprice, .pricenew").text),
                    url=link.get_attribute("href"),
                )
            )
        return products
