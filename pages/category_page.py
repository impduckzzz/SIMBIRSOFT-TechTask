from __future__ import annotations

import allure

from pages.base_catalog_page import BaseCatalogPage


class CategoryPage(BaseCatalogPage):
    @allure.step("Открыть категорию по пути: {path}")
    def open_category(self, path: str):
        """Открывает страницу конкретной категории по её значению path."""
        self.open(f"index.php?rt=product/category&path={path}")
        return self
