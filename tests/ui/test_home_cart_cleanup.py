from __future__ import annotations

import allure
import pytest

from config.test_data import (
    HOME_PAGE_PRODUCTS_TO_ADD,
    MAX_RANDOM_QUANTITY,
    MIN_RANDOM_QUANTITY,
    get_preferred_option_fragments,
)
from framework.utils import sum_money
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_page import ProductPage


@allure.epic("Automation Test Store")
@allure.feature("Cart")
@allure.story("Home page products")
@allure.title("Random home page products can be added, even positions removed and totals recalculated")
@pytest.mark.ui
def test_home_page_cart_cleanup(driver, clean_cart, randomizer_factory):
    rng = randomizer_factory(offset=30)

    with allure.step("Pick five random unique products from the home page"):
        home_page = HomePage(driver).open()
        selected_products = home_page.pick_random_products(HOME_PAGE_PRODUCTS_TO_ADD, rng)
        assert len(selected_products) == HOME_PAGE_PRODUCTS_TO_ADD

    with allure.step("Add the selected products with random quantities"):
        planned_quantities = {}
        for product in selected_products:
            quantity = rng.randint(MIN_RANDOM_QUANTITY, MAX_RANDOM_QUANTITY)
            planned_quantities[product.name] = quantity
            ProductPage(driver).open_by_url(product.url).configure_and_add_to_cart(
                quantity=quantity,
                preferred_option_fragments=get_preferred_option_fragments(product.name),
            )

    cart_page = CartPage(driver).open()
    items_before_removal = cart_page.get_items()
    assert len(items_before_removal) == HOME_PAGE_PRODUCTS_TO_ADD

    with allure.step("Remove even-positioned products from the cart"):
        even_positions = [index for index in range(1, len(items_before_removal) + 1) if index % 2 == 0]
        expected_remaining_names = [
            item.name for index, item in enumerate(items_before_removal, start=1) if index % 2 != 0
        ]
        cart_page.remove_items_by_positions(even_positions)
        items_after_removal = cart_page.get_items()
        assert [item.name for item in items_after_removal] == expected_remaining_names

    with allure.step("Validate cart subtotal and total after removals"):
        summary = cart_page.get_summary()
        assert summary.subtotal == sum_money(item.total_price for item in items_after_removal)
        assert summary.total == summary.subtotal + summary.adjustments
