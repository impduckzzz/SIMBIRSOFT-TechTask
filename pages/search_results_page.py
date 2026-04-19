from __future__ import annotations

from pages.base_catalog_page import BaseCatalogPage


class SearchResultsPage(BaseCatalogPage):
    def get_product_by_position(self, position: int):
        products = self.get_products()
        if position < 1 or position > len(products):
            raise AssertionError(f"Product position {position} is outside available range 1..{len(products)}.")
        return products[position - 1]
