from __future__ import annotations

from collections.abc import Callable
from typing import Literal, TypeAlias, TypeVar

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import SETTINGS

Locator: TypeAlias = tuple[str, str]
T = TypeVar("T")
WaitCondition: TypeAlias = Callable[[WebDriver], T | Literal[False]]


class WaitHelper:
    """Инкапсулирует явные ожидания, используемые в page object'ах."""

    def __init__(self, driver: WebDriver, timeout: int = SETTINGS.explicit_wait) -> None:
        self.driver = driver
        self.timeout = timeout

    def until(self, condition: WaitCondition[T], message: str = "") -> T:
        """Ждёт, пока не выполнится произвольное условие.

        `condition` — вызываемый объект, который принимает `WebDriver`
        и возвращает truthy-результат, когда ожидание выполнено,
        либо `False`, если условие ещё не наступило.
        Обычно сюда передают `expected_conditions` из Selenium
        или собственную `lambda`.
        """
        return WebDriverWait(self.driver, self.timeout).until(condition, message)

    def visible(self, locator: Locator) -> WebElement:
        """Ждёт, пока элемент станет видимым."""
        return self.until(ec.visibility_of_element_located(locator))

    def present(self, locator: Locator) -> WebElement:
        """Ждёт, пока элемент появится в DOM."""
        return self.until(ec.presence_of_element_located(locator))

    def all_present(self, locator: Locator) -> list[WebElement]:
        """Ждёт, пока в DOM появится хотя бы один подходящий элемент."""
        return self.until(ec.presence_of_all_elements_located(locator))

    def clickable(self, locator: Locator) -> WebElement:
        """Ждёт, пока элемент станет кликабельным."""
        return self.until(ec.element_to_be_clickable(locator))

    def all_visible(self, locator: Locator) -> list[WebElement]:
        """Ждёт, пока все найденные элементы станут видимыми."""
        return self.until(ec.visibility_of_all_elements_located(locator))

    def url_contains(self, value: str) -> bool:
        """Ждёт, пока текущий URL не начнёт содержать ожидаемый фрагмент."""
        return self.until(ec.url_contains(value))

    def staleness(self, element: WebElement) -> bool:
        """Ждёт, пока переданный элемент не станет устаревшим."""
        return self.until(ec.staleness_of(element))

    def text_present(self, locator: Locator, value: str) -> bool:
        """Ждёт, пока внутри элемента не появится указанный текст."""
        return self.until(ec.text_to_be_present_in_element(locator, value))

    def document_ready(self) -> bool:
        """Ждёт, пока `document.readyState` не станет `complete`."""
        return self.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
