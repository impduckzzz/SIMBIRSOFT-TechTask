from __future__ import annotations

import random

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from src.models import ProductCard
from src.utils import normalize_space, parse_money, unique_by_url


class HomePage(BasePage):
    relative_url = ""

    SEARCH_INPUT = (By.ID, "filter_keyword")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".button-in-search")
    PRODUCT_NAME_LINKS = (By.CSS_SELECTOR, ".prdocutname")

    @allure.step("Найти товары по запросу: {keyword}")
    def search_for(self, keyword: str):
        """Выполняет поиск по магазину и возвращает объект страницы с результатами."""
        from pages.search_results_page import SearchResultsPage

        self.enter_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        return SearchResultsPage(self.driver)

    @allure.step("Собрать уникальные товары с главной страницы")
    def get_unique_home_products(self) -> list[ProductCard]:
        """Собирает уникальные карточки товаров с главной страницы по их url."""
        products = []
        for link in self.find_all(self.PRODUCT_NAME_LINKS):
            name = normalize_space(link.text)
            href = link.get_attribute("href")
            if not name or not href:
                continue
            card = link.find_element(By.XPATH, "./ancestor::div[contains(@class,'col-md-3')]")
            price = parse_money(card.find_element(By.CSS_SELECTOR, ".oneprice, .pricenew").text)
            products.append(ProductCard(name=name, price=price, url=href))
        return unique_by_url(products, lambda product: product.url)

    @allure.step("Выбрать {count} случайных товаров с главной страницы")
    def pick_random_products(self, count: int, rng: random.Random) -> list[ProductCard]:
        """Возвращает воспроизводимую случайную выборку уникальных товаров с главной страницы."""
        products = self.get_unique_home_products()
        if len(products) < count:
            raise AssertionError(f"Expected at least {count} unique home page products, got {len(products)}.")
        return rng.sample(products, count)
