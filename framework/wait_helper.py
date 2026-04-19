from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import SETTINGS


class WaitHelper:
    def __init__(self, driver: WebDriver, timeout: int | None = None) -> None:
        self.driver = driver
        self.timeout = timeout or SETTINGS.explicit_wait

    def until(self, condition, message: str | None = None):
        return WebDriverWait(self.driver, self.timeout).until(condition, message)

    def visible(self, locator: tuple[str, str]) -> WebElement:
        return self.until(ec.visibility_of_element_located(locator))

    def present(self, locator: tuple[str, str]) -> WebElement:
        return self.until(ec.presence_of_element_located(locator))

    def clickable(self, locator: tuple[str, str]) -> WebElement:
        return self.until(ec.element_to_be_clickable(locator))

    def all_visible(self, locator: tuple[str, str]) -> list[WebElement]:
        return self.until(ec.visibility_of_all_elements_located(locator))

    def url_contains(self, value: str) -> bool:
        return self.until(ec.url_contains(value))

    def staleness(self, element: WebElement) -> bool:
        return self.until(ec.staleness_of(element))

    def text_present(self, locator: tuple[str, str], value: str) -> bool:
        return self.until(ec.text_to_be_present_in_element(locator, value))

    def document_ready(self) -> bool:
        return self.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
