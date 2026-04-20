from __future__ import annotations

import allure

from pages.base_catalog_page import BaseCatalogPage


class CategoryPage(BaseCatalogPage):
    @allure.step("Open category by path: {path}")
    def open_category(self, path: str):
        """Opens a specific category page by its path id."""
        self.open(f"index.php?rt=product/category&path={path}")
        return self
