# UI automation for practice-automation.com

Проект реализует UI-автотесты на `Python + Selenium WebDriver + PyTest` для страницы [`Form Fields`](https://practice-automation.com/form-fields/) с запуском в `Google Chrome`.

Требования ТЗ, которые покрыты в проекте:

- `Python` как основной язык.
- `Chrome` как браузер для Selenium WebDriver.
- `PyTest` как тестовый фреймворк.
- Использование селекторов `ID`, `CSS` и `XPath`.
- Паттерны `Page Object Model`, `Page Factory`, `Fluent Interface`.
- Интеграция `Allure` через `allure-pytest`.

## Структура проекта

```text
.
|-- framework/
|   |-- elements.py
|-- pages/
|   |-- base_page.py
|   |-- form_fields_page.py
|-- tests/
|   |-- test_form_fields.py
|-- allure-results/
|-- artifacts/
|-- conftest.py
|-- pytest.ini
|-- requirements.txt
```

## Архитектура

- `Page Object Model`: страница формы инкапсулирована в `FormFieldsPage`.
- `Page Factory`: элементы страницы описаны как дескрипторы в `framework/elements.py` и лениво создаются при обращении.
- `Fluent Interface`: методы страницы возвращают `self`, поэтому шаги теста можно вызывать цепочкой.

## Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Если Chrome установлен не в стандартное место, можно указать путь через переменную окружения:

```bash
set CHROME_BINARY=C:\Program Files\Google\Chrome\Application\chrome.exe
```

## Запуск тестов

Обычный запуск:

```bash
python -m pytest
```

Headless-режим:

```bash
python -m pytest --headless
```

Запуск с сохранением результатов для Allure:

```bash
python -m pytest --headless --alluredir allure-results
```

Генерация HTML-отчёта Allure:

```bash
allure serve allure-results
```

## Автотесты

- `test_submit_form_successfully`
  Покрывает основной сценарий из ТЗ:
  заполняет `Name`, `Password`, выбирает `Milk` и `Coffee`, выбирает `Yellow`, задаёт значение в `Do you like automation?`, заполняет `Email`, формирует `Message` на основе блока `Automation tools`, нажимает `Submit` и проверяет alert `Message received!`.

- `test_name_is_required`
  Негативный UI-сценарий:
  форма отправляется без заполненного поля `Name`, после чего проверяется отсутствие alert и наличие стандартного браузерного сообщения валидации.

## Тест-кейсы для README

### Позитивный тест-кейс

**Название:** Успешная отправка формы с корректно заполненными данными

**Предусловия:** Открыт `https://practice-automation.com/form-fields/`

**Шаги:**

1. Ввести в поле `Name` валидное значение.
2. Ввести значение в поле `Password`.
3. Выбрать `Milk` и `Coffee`.
4. Выбрать `Yellow`.
5. В поле `Do you like automation?` выбрать любое значение, например `Yes`.
6. В поле `Email` ввести `name@example.com`.
7. В поле `Message` ввести: `Automation tools: 5. Longest tool name: Katalon Studio.`
8. Нажать `Submit`.

**Ожидаемый результат:** Появляется alert с текстом `Message received!`.

### Негативный тест-кейс

**Название:** Отправка формы без обязательного поля `Name`

**Предусловия:** Открыт `https://practice-automation.com/form-fields/`

**Шаги:**

1. Оставить поле `Name` пустым.
2. Заполнить остальные поля валидными значениями.
3. Нажать `Submit`.

**Ожидаемый результат:** Отправка не происходит, alert не появляется, браузер показывает сообщение валидации для обязательного поля `Name`.

## Отчётность

- Для сбора результатов используется `allure-pytest`.
- При падении теста в отчёт прикладывается скриншот страницы.
- В позитивном сценарии в отчёт также прикладывается скриншот заполненной формы перед отправкой.
- В проект уже добавлен пример скриншота HTML-отчёта: `artifacts/allure-report.png`.

Команды для повторной генерации отчёта:

```bash
python -m pytest --headless --alluredir allure-results
allure serve allure-results
```
