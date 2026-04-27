# Автотесты для SimbirSoft TechTask

Проект на `Python` с двумя наборами автотестов:

- UI-тесты для `https://automationteststore.com/`
- API-тесты для локального сервиса из папки `test-service`

## Стек

- `Python 3.10+`
- `pytest`
- `Allure`
- `pytest-xdist`
- `Selenium WebDriver`
- `requests`
- `pydantic`

## Структура проекта

- `config/` - настройки запуска и тестовые данные
- `src/` - общие модели, клиенты, ожидания и вспомогательные утилиты
- `pages/` - UI page object'ы
- `tests/ui/` - UI-тесты
- `tests/api/` - API-тесты
- `test-service/` - локальный API-сервис для второго задания

## Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск UI-тестов

```bash
pytest -m ui
```

## Запуск API-тестов

Перед запуском API-тестов нужно поднять сервис из папки `test-service`.

```bash
pytest -m api
```

## Запуск всех тестов

```bash
pytest
```

## Параллельный запуск

```bash
pytest -n auto
```

Примеры:

```bash
pytest -m ui -n auto
pytest -m api -n auto
```

## Формирование результатов Allure

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

Примеры:

```bash
pytest -m ui --alluredir=allure-results
pytest -m api --alluredir=allure-results
```

## Полезные переменные окружения

### Для UI

- `HEADLESS=true|false`
- `CHROME_BINARY=C:\path\to\chrome.exe`
- `CHROME_BINARY_CANDIDATES=path1;path2`
- `TEST_RANDOM_SEED=20260419`

### Для API

- `API_BASE_URL=http://localhost:8080`
- `API_TIMEOUT=10`

## API-сервис

Локальный сервис находится в папке `test-service`.

Основные endpoint'ы:

- `POST /api/create`
- `GET /api/get/{id}`
- `GET /api/getAll`
- `PATCH /api/patch/{id}`
- `DELETE /api/delete/{id}`

Swagger:

- `http://localhost:8080/api/_/docs/swagger/`
