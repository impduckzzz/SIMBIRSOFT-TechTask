from __future__ import annotations

import allure
import requests
from requests import Response, Session

from config.settings import SETTINGS
from src.api_models import (
    CreatedEntityResponse,
    EntityListResponse,
    EntityRequest,
    EntityResponse,
    NoContentResponse,
)


class EntityApiClient:
    def __init__(self, session: Session | None = None, base_url: str = SETTINGS.api_base_url) -> None:
        self.session = session or requests.Session()
        self.base_url = base_url.rstrip("/")
        self.timeout = SETTINGS.api_timeout

    def _build_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _request(self, method: str, path: str, **kwargs) -> Response:
        return self.session.request(method, self._build_url(path), timeout=self.timeout, **kwargs)

    @staticmethod
    def _assert_status(response: Response, expected_status: int) -> Response:
        if response.status_code != expected_status:
            raise AssertionError(
                f"Expected status {expected_status}, got {response.status_code}. Response: {response.text}"
            )
        return response

    @allure.step("Создать сущность через API")
    def create_entity(self, payload: EntityRequest) -> CreatedEntityResponse:
        response = self._assert_status(
            self._request("POST", "/api/create", json=payload.model_dump(exclude_none=True)),
            200,
        )
        return CreatedEntityResponse(id=int(response.text.strip()))

    @allure.step("Получить сущность по id={entity_id} через API")
    def get_entity(self, entity_id: int) -> EntityResponse:
        response = self._assert_status(self._request("GET", f"/api/get/{entity_id}"), 200)
        return EntityResponse.model_validate(response.json())

    @allure.step("Получить список сущностей через API")
    def get_all_entities(
        self,
        *,
        title: str | None = None,
        verified: bool | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> EntityListResponse:
        params: dict[str, str | int | bool] = {}
        if title is not None:
            params["title"] = title
        if verified is not None:
            params["verified"] = verified
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["perPage"] = per_page

        response = self._assert_status(self._request("GET", "/api/getAll", params=params), 200)
        return EntityListResponse.model_validate(response.json())

    @allure.step("Обновить сущность с id={entity_id} через API")
    def update_entity(self, entity_id: int, payload: EntityRequest) -> NoContentResponse:
        response = self._assert_status(
            self._request("PATCH", f"/api/patch/{entity_id}", json=payload.model_dump(exclude_none=True)),
            204,
        )
        return NoContentResponse(status_code=response.status_code)

    @allure.step("Удалить сущность с id={entity_id} через API")
    def delete_entity(self, entity_id: int) -> NoContentResponse:
        response = self._assert_status(self._request("DELETE", f"/api/delete/{entity_id}"), 204)
        return NoContentResponse(status_code=response.status_code)
