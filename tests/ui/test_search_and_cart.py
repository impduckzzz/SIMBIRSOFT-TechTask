from __future__ import annotations

import allure
import pytest

from config.test_data import (
    MAX_RANDOM_QUANTITY,
    MIN_RANDOM_QUANTITY,
    SEARCH_KEYWORD,
    SEARCH_RESULT_POSITIONS,
    get_preferred_option_fragments,
)
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from src.utils import sum_money


@allure.epic("Automation Test Store")
@allure.feature("Search and cart")
@allure.story("Search results")
@allure.title("Результаты поиска можно добавить в корзину, удвоить количество самого дешёвого товара и сохранить корректные суммы")
@allure.description(
    "Поиск по ключевому слову shirt, сортировка результатов по имени, добавление второго и "
    "третьего товара в корзину со случайным количеством, удвоение количества самого дешёвого "
    "товара и проверка итоговых сумм."
)
@pytest.mark.ui
def test_search_results_cart_total(
    home_page: HomePage,
    product_page: ProductPage,
    cart_page: CartPage,
    clean_cart,
    randomizer_factory,
):
    rng = randomizer_factory(offset=20)

    with allure.step("Найти товары по запросу shirt и отсортировать выдачу по имени"):
        search_results = home_page.search_for(SEARCH_KEYWORD)
        search_results.sort_by_visible_text("Name A - Z")
        products = search_results.get_products()
        assert len(products) >= max(SEARCH_RESULT_POSITIONS)

    selected_products = [products[position - 1] for position in SEARCH_RESULT_POSITIONS]
    selected_quantities = {
        product.name: rng.randint(MIN_RANDOM_QUANTITY, MAX_RANDOM_QUANTITY)
        for product in selected_products
    }

    with allure.step("Добавить второй и третий товар из выдачи со случайным количеством"):
        for product in selected_products:
            product_page.open_by_url(product.url).configure_and_add_to_cart(
                quantity=selected_quantities[product.name],
                preferred_option_fragments=get_preferred_option_fragments(product.name),
            )

    with allure.step("Убедиться, что в корзине находятся оба выбранных товара"):
        cart_page.open()
        cart_items = cart_page.get_items()
        assert len(cart_items) == 2
        assert {item.name.casefold() for item in cart_items} == {
            product.name.casefold() for product in selected_products
        }

    with allure.step("Найти самый дешёвый товар и удвоить его количество"):
        cheapest_item = cart_page.get_cheapest_item()
        cart_page.update_item_quantity(cheapest_item.quantity_input_id, cheapest_item.quantity * 2)
        updated_items = cart_page.get_items()
        updated_cheapest = next(
            item for item in updated_items if item.quantity_input_id == cheapest_item.quantity_input_id
        )
        assert updated_cheapest.quantity == cheapest_item.quantity * 2

    with allure.step("Проверить subtotal и total после обновления корзины"):
        summary = cart_page.get_summary()
        assert summary.subtotal == sum_money(item.total_price for item in updated_items)
        assert summary.total == summary.subtotal + summary.adjustments
