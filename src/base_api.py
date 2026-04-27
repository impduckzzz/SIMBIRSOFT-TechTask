from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import TypeVar

import requests
from requests import Response, Session

from config.settings import SETTINGS

F = TypeVar("F", bound=Callable[..., Response])


def expect_status(expected_status: int):
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Response:
            response = func(*args, **kwargs)
            if response.status_code != expected_status:
                raise AssertionError(
                    f"Expected status {expected_status}, got {response.status_code}. Response: {response.text}"
                )
            return response

        return wrapper  # type: ignore[return-value]

    return decorator


class BaseApi:
    def __init__(self, session: Session | None = None, base_url: str = SETTINGS.api_base_url) -> None:
        self.session = session or requests.Session()
        self.base_url = base_url.rstrip("/")
        self.timeout = SETTINGS.api_timeout

    def _build_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _request(self, method: str, path: str, **kwargs) -> Response:
        return self.session.request(method, self._build_url(path), timeout=self.timeout, **kwargs)
