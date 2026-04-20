from __future__ import annotations

from decimal import Decimal

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from src.models import CartItem, CartSummary
from src.utils import MONEY_ZERO, normalize_space, parse_money, sum_money


class CartPage(BasePage):
    relative_url = "index.php?rt=checkout/cart"

    CART_TABLE = (By.CSS_SELECTOR, "#cart table.table")
    CART_ROWS = (By.CSS_SELECTOR, "#cart table.table tbody tr")
    REMOVE_LINKS = (By.CSS_SELECTOR, "#cart table.table a.btn.btn-sm.btn-default")
    UPDATE_BUTTON = (By.ID, "cart_update")
    TOTALS_TABLE = (By.ID, "totals_table")

    @allure.step("Check whether the cart is empty")
    def is_empty(self) -> bool:
        """Returns True when the cart page contains the empty cart message."""
        return "Your shopping cart is empty!" in self.driver.page_source

    @allure.step("Clear cart content")
    def clear(self) -> None:
        """Removes all items from the cart one by one."""
        self.open()
        while not self.is_empty():
            remove_links = [link.get_attribute("href") for link in self.find_all(self.REMOVE_LINKS)]
            if not remove_links:
                break
            self.driver.get(remove_links[0])
            self.wait_until_ready()

    @allure.step("Read current cart items")
    def get_items(self) -> list[CartItem]:
        """Parses all product rows from the cart table into structured models."""
        if self.is_empty():
            return []

        rows = [
            row
            for row in self.find_all(self.CART_ROWS)
            if len(row.find_elements(By.TAG_NAME, "td")) >= 7
        ]
        items: list[CartItem] = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            quantity_input = cells[4].find_element(By.TAG_NAME, "input")
            items.append(
                CartItem(
                    name=normalize_space(cells[1].find_element(By.TAG_NAME, "a").text),
                    unit_price=parse_money(cells[3].text),
                    quantity=int(quantity_input.get_attribute("value")),
                    total_price=parse_money(cells[5].text),
                    quantity_input_id=quantity_input.get_attribute("id"),
                    remove_url=cells[6].find_element(By.TAG_NAME, "a").get_attribute("href"),
                    options=tuple(
                        normalize_space(option.text) for option in cells[1].find_elements(By.TAG_NAME, "small")
                    ),
                )
            )
        return items

    @allure.step("Update cart item quantity to {quantity}")
    def update_item_quantity(self, quantity_input_id: str, quantity: int):
        """Changes quantity for a specific cart row and applies the update."""
        quantity_input = self.driver.find_element(By.ID, quantity_input_id)
        self.replace_value(quantity_input, quantity)
        update_button = self.find(self.UPDATE_BUTTON)
        update_button.click()
        self.waits.staleness(quantity_input)
        self.wait_until_ready()
        return self

    @allure.step("Remove cart items by positions: {positions}")
    def remove_items_by_positions(self, positions: list[int]):
        """Removes cart rows by their one-based position in the items table."""
        items = self.get_items()
        remove_urls = [item.remove_url for index, item in enumerate(items, start=1) if index in positions]
        for remove_url in remove_urls:
            self.driver.get(remove_url)
            self.wait_until_ready()
        return self

    @allure.step("Find the cheapest cart item")
    def get_cheapest_item(self) -> CartItem:
        """Returns the cart item with the minimal unit price."""
        items = self.get_items()
        if not items:
            raise AssertionError("Cart is empty.")
        return min(items, key=lambda item: item.unit_price)

    @allure.step("Read cart summary values")
    def get_summary(self) -> CartSummary:
        """Builds subtotal, adjustments and total values from the totals table."""
        if self.is_empty():
            return CartSummary(subtotal=MONEY_ZERO, adjustments=MONEY_ZERO, total=MONEY_ZERO, breakdown={})

        breakdown: dict[str, Decimal] = {}
        for row in self.find(self.TOTALS_TABLE).find_elements(By.CSS_SELECTOR, "tbody tr"):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 2:
                continue
            label = normalize_space(cells[0].text).rstrip(":")
            amount = parse_money(cells[1].text)
            breakdown[label] = amount

        subtotal = breakdown.get("Sub-Total", MONEY_ZERO)
        total = breakdown.get("Total", MONEY_ZERO)
        adjustments = sum_money(
            amount for label, amount in breakdown.items() if label not in {"Sub-Total", "Total"}
        )
        return CartSummary(subtotal=subtotal, adjustments=adjustments, total=total, breakdown=breakdown)
