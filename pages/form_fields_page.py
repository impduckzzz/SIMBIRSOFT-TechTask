from __future__ import annotations

import allure
from selenium.webdriver.common.by import By

from framework.elements import PageFactory
from pages.base_page import BasePage


class FormFieldsPage(BasePage):
    path = "/form-fields/"

    feedback_form = PageFactory.element(By.ID, "feedbackForm", "Feedback form")
    name_input = PageFactory.element(By.ID, "name-input", "Name input")
    password_input = PageFactory.element(
        By.CSS_SELECTOR,
        "#feedbackForm input[type='password']",
        "Password input",
    )
    automation_select = PageFactory.element(By.ID, "automation", "Automation select")
    email_input = PageFactory.element(By.ID, "email", "Email input")
    message_input = PageFactory.element(By.ID, "message", "Message textarea")
    submit_button = PageFactory.element(By.ID, "submit-btn", "Submit button")
    drinks = PageFactory.checkbox_group(
        By.XPATH,
        "//input[@name='fav_drink' and @value='{option}']",
        "Favorite drink",
    )
    colors = PageFactory.checkbox_group(
        By.XPATH,
        "//input[@name='fav_color' and @value='{option}']",
        "Favorite color",
    )

    AUTOMATION_TOOLS = (
        "Selenium",
        "Playwright",
        "Cypress",
        "Appium",
        "Katalon Studio",
    )

    @allure.step("Open the Form Fields page")
    def open(self):
        super().open()
        self.feedback_form.find()
        return self

    @allure.step("Fill Name with: {value}")
    def fill_name(self, value: str):
        self.name_input.type(value)
        return self

    @allure.step("Fill Password")
    def fill_password(self, value: str):
        self.password_input.type(value)
        return self

    @allure.step("Select favorite drinks: {values}")
    def select_drinks(self, *values: str):
        for value in values:
            self.drinks.resolve(self, value).check()
        return self

    @allure.step("Select favorite color: {value}")
    def select_color(self, value: str):
        self.colors.resolve(self, value).check()
        return self

    @allure.step("Select automation preference: {value}")
    def choose_automation(self, value: str):
        self.automation_select.select_by_text(value)
        return self

    @allure.step("Fill Email with: {value}")
    def fill_email(self, value: str):
        self.email_input.type(value)
        return self

    @allure.step("Fill Message field")
    def fill_message(self, value: str):
        self.message_input.type(value)
        return self

    @allure.step("Submit the form")
    def submit(self):
        self.submit_button.click()
        return self

    @allure.step("Accept success alert")
    def accept_success_alert(self) -> str:
        alert = self.wait_for_alert()
        text = alert.text
        alert.accept()
        return text

    @allure.step("Get browser validation message for Name field")
    def name_validation_message(self) -> str:
        return self.validation_message(self.name_input)

    def build_message_for_task(self) -> str:
        tools_count = len(self.AUTOMATION_TOOLS)
        longest_tool = max(self.AUTOMATION_TOOLS, key=len)
        return f"Automation tools: {tools_count}. Longest tool name: {longest_tool}."
