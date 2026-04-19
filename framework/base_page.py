from __future__ import annotations

from urllib.parse import urljoin

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from config.settings import SETTINGS
from framework.wait_helper import WaitHelper


class BasePage:
    relative_url = ""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.waits = WaitHelper(driver)

    def open(self, relative_url: str | None = None):
        target = urljoin(SETTINGS.base_url, relative_url or self.relative_url)
        self.driver.get(target)
        self.wait_until_ready()
        return self

    def wait_until_ready(self) -> None:
        self.waits.document_ready()

    def find(self, locator: tuple[str, str]) -> WebElement:
        return self.waits.visible(locator)

    def find_all(self, locator: tuple[str, str]) -> list[WebElement]:
        return self.driver.find_elements(*locator)

    def click(self, locator: tuple[str, str]) -> WebElement:
        element = self.waits.clickable(locator)
        element.click()
        return element

    def type(self, locator: tuple[str, str], value: str, clear: bool = True) -> WebElement:
        element = self.find(locator)
        if clear:
            element.clear()
        element.send_keys(value)
        return element

    def replace_value(self, element: WebElement, value: str | int) -> WebElement:
        element.send_keys(Keys.CONTROL, "a", Keys.DELETE)
        element.send_keys(str(value))
        return element

    def scroll_into_view(self, element: WebElement) -> None:
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )

    def select_by_visible_text(self, locator: tuple[str, str], value: str) -> str:
        select = Select(self.find(locator))
        select.select_by_visible_text(value)
        return value
