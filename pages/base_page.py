from __future__ import annotations

from urllib.parse import urljoin

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    path = "/"

    def __init__(self, driver, base_url: str, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(urljoin(self.base_url, self.path))
        return self

    def wait_for_visible(self, locator):
        return self.wait.until(ec.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(ec.element_to_be_clickable(locator))

    def wait_for_presence(self, locator):
        return self.wait.until(ec.presence_of_element_located(locator))

    def wait_for_alert(self) -> Alert:
        return self.wait.until(ec.alert_is_present())

    def is_alert_present(self, timeout: int = 2) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(ec.alert_is_present())
            return True
        except TimeoutException:
            return False

    def validation_message(self, element) -> str:
        return element.attribute("validationMessage")

    def take_screenshot(self) -> bytes:
        return self.driver.get_screenshot_as_png()
