from __future__ import annotations

import allure

from pages.base_catalog_page import BaseCatalogPage


class SearchResultsPage(BaseCatalogPage):
    @allure.step("Get product from search results by position: {position}")
    def get_product_by_position(self, position: int):
        """Returns a product by its one-based position in the current results list."""
        products = self.get_products()
        if position < 1 or position > len(products):
            raise AssertionError(f"Product position {position} is outside available range 1..{len(products)}.")
        return products[position - 1]
