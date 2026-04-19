from __future__ import annotations

from pages.base_catalog_page import BaseCatalogPage


class CategoryPage(BaseCatalogPage):
    def open_category(self, path: str):
        self.open(f"index.php?rt=product/category&path={path}")
        return self
