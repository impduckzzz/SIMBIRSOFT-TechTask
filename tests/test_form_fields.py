from __future__ import annotations

import allure
import pytest

from pages.form_fields_page import FormFieldsPage


@pytest.mark.ui
@allure.epic("Practice Automation")
@allure.feature("Form Fields")
class TestFormFields:
    @allure.title("Submit the Form Fields page successfully")
    def test_submit_form_successfully(self, form_fields_page: FormFieldsPage):
        page = (
            form_fields_page.open()
            .fill_name("Alex QA")
            .fill_password("P@ssw0rd!")
            .select_drinks("Milk", "Coffee")
            .select_color("Yellow")
            .choose_automation("Yes")
            .fill_email("name@example.com")
            .fill_message(form_fields_page.build_message_for_task())
        )

        allure.attach(
            page.take_screenshot(),
            name="filled-form",
            attachment_type=allure.attachment_type.PNG,
        )

        alert_text = page.submit().accept_success_alert()

        assert alert_text == "Message received!"

    @allure.title("Prevent submission when the required Name field is empty")
    def test_name_is_required(self, form_fields_page: FormFieldsPage):
        page = (
            form_fields_page.open()
            .fill_password("P@ssw0rd!")
            .select_drinks("Milk", "Coffee")
            .select_color("Yellow")
            .choose_automation("Yes")
            .fill_email("name@example.com")
            .fill_message(form_fields_page.build_message_for_task())
            .submit()
        )

        assert not page.is_alert_present()
        assert page.name_validation_message()
