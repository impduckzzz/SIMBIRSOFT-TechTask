from __future__ import annotations

import os
from pathlib import Path

import allure
import pytest
from _pytest.fixtures import FixtureRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.form_fields_page import FormFieldsPage

PROJECT_ROOT = Path(__file__).resolve().parent


def resolve_chrome_binary() -> str | None:
    candidates = [
        Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
        Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
        Path.home() / "AppData/Local/Google/Chrome/Application/chrome.exe",
    ]

    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)

    return None


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--base-url",
        action="store",
        default="https://practice-automation.com",
        help="Base URL for UI tests.",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode.",
    )


@pytest.fixture
def driver(request: FixtureRequest):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--window-size=1920,1080")

    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")

    cache_path = os.getenv("SE_CACHE_PATH")
    if not cache_path:
        local_cache = PROJECT_ROOT / ".selenium-cache"
        local_cache.mkdir(exist_ok=True)
        os.environ["SE_CACHE_PATH"] = str(local_cache)

    chrome_binary = os.getenv("CHROME_BINARY") or resolve_chrome_binary()
    if chrome_binary:
        options.binary_location = chrome_binary

    driver_instance = webdriver.Chrome(options=options)
    yield driver_instance
    driver_instance.quit()


@pytest.fixture
def form_fields_page(driver, request: FixtureRequest) -> FormFieldsPage:
    base_url = request.config.getoption("--base-url")
    return FormFieldsPage(driver, base_url)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    driver = item.funcargs.get("driver")
    if not driver:
        return

    allure.attach(
        driver.get_screenshot_as_png(),
        name=f"{item.name}-failure",
        attachment_type=allure.attachment_type.PNG,
    )
