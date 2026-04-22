from __future__ import annotations

import allure
import pytest

from config.test_data import (
    HOME_PAGE_PRODUCTS_TO_ADD,
    MAX_RANDOM_QUANTITY,
    MIN_RANDOM_QUANTITY,
    get_preferred_option_fragments,
)
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from src.utils import sum_money


@allure.epic("Automation Test Store")
@allure.feature("Cart")
@allure.story("Home page products")
@allure.title("Случайные товары с главной страницы можно добавить, удалить чётные позиции и пересчитать итоговые суммы")
@allure.description(
    "Добавление пяти случайных товаров с главной страницы в корзину со случайным количеством, "
    "удаление товаров на чётных позициях и проверка итоговых сумм."
)
@pytest.mark.ui
def test_home_page_cart_cleanup(
    home_page: HomePage,
    product_page: ProductPage,
    cart_page: CartPage,
    clean_cart,
    randomizer_factory,
):
    rng = randomizer_factory(offset=30)

    with allure.step("Выбрать пять случайных уникальных товаров с главной страницы"):
        selected_products = home_page.pick_random_products(HOME_PAGE_PRODUCTS_TO_ADD, rng)
        assert len(selected_products) == HOME_PAGE_PRODUCTS_TO_ADD

    with allure.step("Добавить выбранные товары в корзину со случайным количеством"):
        planned_quantities = {}
        for product in selected_products:
            quantity = rng.randint(MIN_RANDOM_QUANTITY, MAX_RANDOM_QUANTITY)
            planned_quantities[product.name] = quantity
            product_page.open_by_url(product.url).configure_and_add_to_cart(
                quantity=quantity,
                preferred_option_fragments=get_preferred_option_fragments(product.name),
            )

    with allure.step("Убедиться, что все пять товаров добавлены в корзину"):
        cart_page.open()
        items_before_removal = cart_page.get_items()
        assert len(items_before_removal) == HOME_PAGE_PRODUCTS_TO_ADD

    with allure.step("Удалить товары на чётных позициях в таблице корзины"):
        even_positions = [index for index in range(1, len(items_before_removal) + 1) if index % 2 == 0]
        expected_remaining_names = [
            item.name for index, item in enumerate(items_before_removal, start=1) if index % 2 != 0
        ]
        cart_page.remove_items_by_positions(even_positions)
        items_after_removal = cart_page.get_items()
        assert [item.name for item in items_after_removal] == expected_remaining_names

    with allure.step("Проверить subtotal и total после удаления чётных позиций"):
        summary = cart_page.get_summary()
        assert summary.subtotal == sum_money(item.total_price for item in items_after_removal)
        assert summary.total == summary.subtotal + summary.adjustments
