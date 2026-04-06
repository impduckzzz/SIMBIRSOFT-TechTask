from __future__ import annotations

from typing import Iterable

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select


class PageElement:
    def __init__(self, page, locator: tuple[str, str], name: str):
        self.page = page
        self.locator = locator
        self.name = name

    def find(self) -> WebElement:
        return self.page.wait_for_visible(self.locator)

    def type(self, text: str, clear_first: bool = True) -> "PageElement":
        element = self.find()
        if clear_first:
            element.clear()
        element.send_keys(text)
        return self

    def click(self) -> "PageElement":
        element = self.page.wait_for_clickable(self.locator)
        self.page.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )

        try:
            element.click()
        except ElementClickInterceptedException:
            self.page.driver.execute_script("arguments[0].click();", element)
        return self

    def check(self) -> "PageElement":
        element = self.find()
        if not element.is_selected():
            element.click()
        return self

    def select_by_text(self, text: str) -> "PageElement":
        Select(self.find()).select_by_visible_text(text)
        return self

    def options_text(self) -> list[str]:
        return [option.text.strip() for option in Select(self.find()).options if option.text.strip()]

    def text(self) -> str:
        return self.find().text.strip()

    def value(self) -> str:
        return self.find().get_attribute("value")

    def attribute(self, name: str) -> str:
        return self.find().get_attribute(name)


class PageElementDescriptor:
    def __init__(self, by: str, value: str, name: str):
        self.locator = (by, value)
        self.name = name

    def __get__(self, instance, owner) -> PageElement | "PageElementDescriptor":
        if instance is None:
            return self
        return PageElement(instance, self.locator, self.name)


class PageFactory:
    @staticmethod
    def element(by: str, value: str, name: str) -> PageElementDescriptor:
        return PageElementDescriptor(by, value, name)

    @staticmethod
    def checkbox_group(by: str, value_template: str, name: str):
        def resolver(option_text: str) -> tuple[str, str]:
            return by, value_template.format(option=option_text)

        return GroupedElementFactory(resolver, name)


class GroupedElementFactory:
    def __init__(self, resolver, name: str):
        self.resolver = resolver
        self.name = name

    def resolve(self, page, option_text: str) -> PageElement:
        return PageElement(page, self.resolver(option_text), f"{self.name}: {option_text}")
