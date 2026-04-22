from __future__ import annotations

import random
import sys
from pathlib import Path

import allure
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.settings import SETTINGS
from config.test_data import CATEGORY_PATH
from pages.cart_page import CartPage
from pages.category_page import CategoryPage
from pages.home_page import HomePage
from src.driver_utils import build_driver


@pytest.fixture()
def driver(request):
    web_driver = build_driver()
    yield web_driver
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        allure.attach(
            web_driver.get_screenshot_as_png(),
            name="failure-screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            web_driver.page_source,
            name="page-source",
            attachment_type=allure.attachment_type.HTML,
        )
        allure.attach(
            web_driver.current_url,
            name="current-url",
            attachment_type=allure.attachment_type.TEXT,
        )
    web_driver.quit()


@pytest.fixture()
def home_page(driver, clean_cart) -> HomePage:
    return HomePage(driver).open()


@pytest.fixture()
def category_page(driver) -> CategoryPage:
    return CategoryPage(driver).open_category(CATEGORY_PATH)


@pytest.fixture()
def clean_cart(driver):
    cart_page = CartPage(driver)
    cart_page.clear_cart()
    yield cart_page


@pytest.fixture()
def randomizer_factory():
    def _factory(offset: int = 0) -> random.Random:
        return random.Random(SETTINGS.random_seed + offset)

    return _factory


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
