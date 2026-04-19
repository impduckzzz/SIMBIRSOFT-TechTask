from __future__ import annotations

from collections.abc import Iterable

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from framework.base_page import BasePage
from framework.utils import normalize_space


class ProductPage(BasePage):
    PRODUCT_FORM = (By.ID, "product")
    PRODUCT_NAME = (By.CSS_SELECTOR, "span.bgnone")
    QUANTITY_INPUT = (By.ID, "product_quantity")
    OPTION_SELECTS = (By.CSS_SELECTOR, "#product select")
    OPTION_RADIOS = (By.CSS_SELECTOR, "#product input[type='radio']")

    def open_by_url(self, url: str):
        self.driver.get(url)
        self.wait_until_ready()
        self.find(self.PRODUCT_FORM)
        return self

    def get_name(self) -> str:
        return normalize_space(self.find(self.PRODUCT_NAME).text)

    def configure_and_add_to_cart(
        self,
        quantity: int,
        preferred_option_fragments: Iterable[str] | None = None,
    ):
        preferred_fragments = list(preferred_option_fragments or [])
        self._select_available_dropdown_options(preferred_fragments)
        self._select_available_radio_options(preferred_fragments)
        self.replace_value(self.find(self.QUANTITY_INPUT), quantity)
        form = self.find(self.PRODUCT_FORM)
        form.submit()
        self.waits.url_contains("rt=checkout/cart")
        from pages.cart_page import CartPage

        return CartPage(self.driver)

    def _select_available_dropdown_options(self, preferred_fragments: list[str]) -> None:
        for select_element in self.find_all(self.OPTION_SELECTS):
            select = Select(select_element)
            option_texts = [normalize_space(option.text) for option in select.options]
            matching_choice = self._pick_matching_option(option_texts, preferred_fragments)
            if matching_choice is None:
                matching_choice = self._pick_first_available_option(option_texts)
            if matching_choice is None:
                raise AssertionError(
                    f"No selectable in-stock value found for dropdown '{select_element.get_attribute('id')}'."
                )
            select.select_by_visible_text(matching_choice)

    def _select_available_radio_options(self, preferred_fragments: list[str]) -> None:
        radio_groups: dict[str, list[tuple[str, object]]] = {}
        for radio in self.find_all(self.OPTION_RADIOS):
            group_name = radio.get_attribute("name")
            label = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{radio.get_attribute('id')}']")
            label_text = normalize_space(label.text)
            radio_groups.setdefault(group_name, []).append((label_text, radio))

        for radio_group in radio_groups.values():
            option_texts = [text for text, _ in radio_group]
            matching_choice = self._pick_matching_option(option_texts, preferred_fragments)
            if matching_choice is None:
                matching_choice = self._pick_first_available_option(option_texts)
            if matching_choice is None:
                raise AssertionError("No selectable radio option is available for the current product.")
            for option_text, radio in radio_group:
                if option_text == matching_choice:
                    if not radio.is_selected():
                        radio.click()
                    break

    @staticmethod
    def _pick_matching_option(
        option_texts: list[str],
        preferred_fragments: list[str],
    ) -> str | None:
        for fragment in preferred_fragments:
            for option_text in option_texts:
                if fragment.lower() in option_text.lower() and "out of stock" not in option_text.lower():
                    preferred_fragments.remove(fragment)
                    return option_text
        return None

    @staticmethod
    def _pick_first_available_option(option_texts: list[str]) -> str | None:
        for option_text in option_texts:
            normalized = option_text.lower()
            if not option_text or "------" in normalized or "out of stock" in normalized:
                continue
            return option_text
        return None
