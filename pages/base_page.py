from __future__ import annotations

from urllib.parse import urljoin

import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from config.settings import SETTINGS
from src.wait_helper import Locator, WaitHelper


class BasePage:
    relative_url = ""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.waits = WaitHelper(driver)

    @allure.step("Открыть страницу: {relative_url}")
    def open(self, relative_url: str | None = None):
        """Открывает либо URL страницы по умолчанию, либо переданный относительный путь."""
        relative_url = self.relative_url if relative_url is None else relative_url
        url = urljoin(SETTINGS.base_url, relative_url) if relative_url else SETTINGS.base_url
        self.driver.get(url)
        self.wait_until_ready()
        return self

    @allure.step("Дождаться готовности документа")
    def wait_until_ready(self) -> None:
        """Ждёт, пока `document.readyState` не станет `complete`."""
        self.waits.document_ready()

    @allure.step("Найти видимый элемент по локатору: {locator}")
    def find(self, locator: Locator) -> WebElement:
        """Находит видимый элемент на странице."""
        return self.waits.visible(locator)

    @allure.step("Найти все элементы по локатору: {locator}")
    def find_all(self, locator: Locator) -> list[WebElement]:
        """Ждёт готовности документа и затем возвращает все найденные элементы, включая пустой список."""
        self.waits.document_ready()
        return self.driver.find_elements(*locator)

    @allure.step("Кликнуть по элементу: {locator}")
    def click(self, locator: Locator) -> WebElement:
        """Ждёт кликабельности элемента и выполняет клик."""
        element = self.waits.clickable(locator)
        element.click()
        return element

    @allure.step("Ввести текст '{value}' в поле: {locator}")
    def enter_text(self, locator: Locator, value: str, clear: bool = True) -> WebElement:
        """Вводит текст в поле и при необходимости предварительно очищает его."""
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
    def select_by_visible_text(self, locator: Locator, value: str) -> str:
        """Выбирает значение в выпадающем списке по видимому тексту."""
        select = Select(self.find(locator))
        select.select_by_visible_text(value)
        return value
