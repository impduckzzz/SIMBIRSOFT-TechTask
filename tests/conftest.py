from __future__ import annotations

import random
import sys
from pathlib import Path

import allure
import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.api_test_data import build_entity_request
from config.settings import SETTINGS
from config.test_data import CATEGORY_PATH
from pages.cart_page import CartPage
from pages.category_page import CategoryPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from src.api_client import EntityApiClient
from src.api_models import CreatedEntityResponse, EntityRequest
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
def api_client() -> EntityApiClient:
    return EntityApiClient()


@pytest.fixture()
def entity_request_factory():
    def _factory(**kwargs) -> EntityRequest:
        return build_entity_request(**kwargs)

    return _factory


@pytest.fixture()
def cart_page(driver) -> CartPage:
    return CartPage(driver)


@pytest.fixture()
def product_page(driver) -> ProductPage:
    return ProductPage(driver)


@pytest.fixture()
def clean_cart(cart_page: CartPage):
    cart_page.clear_cart()
    yield cart_page


@pytest.fixture()
def randomizer_factory():
    def _factory(offset: int = 0) -> random.Random:
        return random.Random(SETTINGS.random_seed + offset)

    return _factory


@pytest.fixture()
def created_entity(api_client: EntityApiClient, entity_request_factory):
    payload = entity_request_factory()
    created = api_client.create_entity(payload)
    yield payload, created
    try:
        requests.delete(
            f"{SETTINGS.api_base_url.rstrip('/')}/api/delete/{created.id}",
            timeout=SETTINGS.api_timeout,
        )
    except requests.RequestException:
        pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
