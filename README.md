# UI-автотесты для Automation Test Store

Проект UI-автоматизации на `Python + Selenium` для сайта https://automationteststore.com/.

## Стек

- `Python 3.10+`
- `Selenium WebDriver`
- `pytest`
- `Allure`
- `pytest-xdist`

## Структура проекта

- `config/` - настройки запуска и статические тестовые данные
- `framework/` - фабрика драйвера, ожидания, модели и общие хелперы
- `pages/` - классы `Page Object Model`
- `tests/` - автоматизированные UI-тесты
- `docs/test_cases.md` - подробные тест-кейсы по чек-листу

## Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск тестов

```bash
pytest -m ui
```

## Параллельный запуск

```bash
pytest -m ui -n auto
```

## Формирование результатов Allure

```bash
pytest -m ui -n auto --alluredir=allure-results
allure serve allure-results
```

## Полезные переменные окружения

- `HEADLESS=true|false`
- `CHROME_BINARY=C:\path\to\chrome.exe`
- `TEST_RANDOM_SEED=20260419`
