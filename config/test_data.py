from __future__ import annotations


CATEGORY_PATH = "68"
SEARCH_KEYWORD = "shirt"
SEARCH_RESULT_POSITIONS = (2, 3)
HOME_PAGE_PRODUCTS_TO_ADD = 5
MIN_RANDOM_QUANTITY = 1
MAX_RANDOM_QUANTITY = 3

# Option preferences are applied dynamically only when the target product
# exposes matching values. Otherwise the framework falls back to the first
# in-stock option to keep tests resilient.
_PREFERRED_OPTION_FRAGMENTS = {
    "Designer Men Casual Formal Double Cuffs Grandad Band Collar Shirt Elegant Tie": [
        "Light Blue",
        "Medium",
    ],
    "Fruit of the Loom T-Shirts 5 Pack - Super Premium": [
        "Medium",
    ],
    "Casual 3/4 Sleeve Baseball T-Shirt": [
        "Yellow",
    ],
}


def get_preferred_option_fragments(product_name: str) -> list[str] | None:
    for known_name, fragments in _PREFERRED_OPTION_FRAGMENTS.items():
        if known_name.casefold() == product_name.casefold():
            return list(fragments)
    return None
