from __future__ import annotations

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import SETTINGS


def _resolve_chrome_binary() -> str | None:
    """Возвращает путь к Chrome из настроек, если он задан и существует."""
    if SETTINGS.chrome_binary:
        configured_path = Path(SETTINGS.chrome_binary)
        if configured_path.exists():
            return str(configured_path)

    for candidate in SETTINGS.chrome_binary_candidates:
        candidate_path = Path(candidate)
        if candidate_path.exists():
            return str(candidate_path)

    return None


def build_driver() -> WebDriver:
    """Создаёт и настраивает экземпляр Chrome WebDriver для UI-тестов."""
    if SETTINGS.browser != "chrome":
        raise ValueError(f"Unsupported browser '{SETTINGS.browser}'. Only chrome is configured.")

    options = ChromeOptions()
    chrome_binary = _resolve_chrome_binary()
    if chrome_binary:
        options.binary_location = chrome_binary

    options.add_argument(f"--window-size={SETTINGS.window_size}")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument("--lang=en-US")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--remote-allow-origins=*")
    if SETTINGS.headless:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(SETTINGS.page_load_timeout)
    return driver
