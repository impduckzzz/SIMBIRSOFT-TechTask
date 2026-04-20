from __future__ import annotations

from urllib.parse import urljoin

import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from config.settings import SETTINGS
from src.wait_helper import WaitHelper


class BasePage:
    relative_url = ""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.waits = WaitHelper(driver)

    @allure.step("Открыть страницу: {relative_url}")
    def open(self, relative_url: str | None = None):
        """Открывает либо url страницы по умолчанию, либо переданный относительный путь."""
        target = urljoin(SETTINGS.base_url, relative_url or self.relative_url)
        self.driver.get(target)
        self.wait_until_ready()
        return self

    @allure.step("Дождаться полной загрузки страницы")
    def wait_until_ready(self) -> None:
        """Ждёт, пока браузер сообщит о полной готовности документа."""
        self.waits.document_ready()

    @allure.step("Найти видимый элемент по локатору: {locator}")
    def find(self, locator: tuple[str, str]) -> WebElement:
        """Находит видимый элемент на странице."""
        return self.waits.visible(locator)

    @allure.step("Найти все элементы по локатору: {locator}")
    def find_all(self, locator: tuple[str, str]) -> list[WebElement]:
        """Ждёт готовности страницы и затем возвращает все найденные элементы, включая пустой список."""
        self.waits.document_ready()
        return self.driver.find_elements(*locator)

    @allure.step("Кликнуть по элементу: {locator}")
    def click(self, locator: tuple[str, str]) -> WebElement:
        """Ждёт кликабельности элемента и выполняет клик."""
        element = self.waits.clickable(locator)
        element.click()
        return element

    @allure.step("Ввести '{value}' в элемент: {locator}")
    def type(self, locator: tuple[str, str], value: str, clear: bool = True) -> WebElement:
        """Вводит значение в поле и при необходимости предварительно очищает его."""
        element = self.find(locator)
        if clear:
            element.clear()
        element.send_keys(value)
        return element

    @allure.step("Заменить значение элемента на: {value}")
    def replace_value(self, element: WebElement, value: str | int) -> WebElement:
        """Выделяет текущее значение в поле и заменяет его новым."""
        element.send_keys(Keys.CONTROL, "a", Keys.DELETE)
        element.send_keys(str(value))
        return element

    @allure.step("Прокрутить страницу до элемента")
    def scroll_into_view(self, element: WebElement) -> None:
        """Прокручивает страницу так, чтобы элемент оказался по центру области просмотра."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )

    @allure.step("Выбрать '{value}' в выпадающем списке: {locator}")
    def select_by_visible_text(self, locator: tuple[str, str], value: str) -> str:
        """Выбирает значение в выпадающем списке по видимому тексту."""
        select = Select(self.find(locator))
        select.select_by_visible_text(value)
        return value
