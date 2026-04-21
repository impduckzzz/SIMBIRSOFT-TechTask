from __future__ import annotations

import allure
import pytest

from config.test_data import CATEGORY_PATH
from pages.category_page import CategoryPage


@pytest.fixture()
def category_page(driver) -> CategoryPage:
    return CategoryPage(driver).open_category(CATEGORY_PATH)


@allure.epic("Automation Test Store")
@allure.feature("Catalog")
@allure.story("Category sorting")
@allure.title("Category products can be sorted by name and price in both directions")
@allure.description(
    "Проверка сортировки товаров в категории Apparel & Accessories по имени и цене "
    "в обоих направлениях."
)
@pytest.mark.ui
def test_category_products_are_sorted_by_name_and_price(category_page: CategoryPage):
    with allure.step("Убедиться, что в категории есть минимум четыре товара"):
        products = category_page.get_products()
        assert len(products) >= 4, "The chosen category should contain at least four products."

    with allure.step("Проверить сортировку по имени по возрастанию"):
        category_page.sort_by_visible_text("Name A - Z")
        names_ascending = [product.name.casefold() for product in category_page.get_products()]
        assert names_ascending == sorted(names_ascending)

    with allure.step("Проверить сортировку по имени по убыванию"):
        category_page.sort_by_visible_text("Name Z - A")
        names_descending = [product.name.casefold() for product in category_page.get_products()]
        assert names_descending == sorted(names_descending, reverse=True)

    with allure.step("Проверить сортировку по цене по возрастанию"):
        category_page.sort_by_visible_text("Price Low > High")
        prices_ascending = [product.price for product in category_page.get_products()]
        assert prices_ascending == sorted(prices_ascending)

    with allure.step("Проверить сортировку по цене по убыванию"):
        category_page.sort_by_visible_text("Price High > Low")
        prices_descending = [product.price for product in category_page.get_products()]
        assert prices_descending == sorted(prices_descending, reverse=True)
