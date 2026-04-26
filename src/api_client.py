from __future__ import annotations

import allure
from requests import Response

from src.api_models import (
    CreatedEntityResponse,
    EntityListResponse,
    EntityRequest,
    EntityResponse,
    NoContentResponse,
)
from src.base_api import BaseApi, expect_status


class EntityApiClient(BaseApi):
    @expect_status(200)
    def _create_entity_response(self, payload: EntityRequest) -> Response:
        return self._request("POST", "/api/create", json=payload.model_dump(exclude_none=True))

    @expect_status(200)
    def _get_entity_response(self, entity_id: int) -> Response:
        return self._request("GET", f"/api/get/{entity_id}")

    @expect_status(200)
    def _get_all_entities_response(self, params: dict[str, str | int | bool]) -> Response:
        return self._request("GET", "/api/getAll", params=params)

    @expect_status(204)
    def _update_entity_response(self, entity_id: int, payload: EntityRequest) -> Response:
        return self._request("PATCH", f"/api/patch/{entity_id}", json=payload.model_dump(exclude_none=True))

    @expect_status(204)
    def _delete_entity_response(self, entity_id: int) -> Response:
        return self._request("DELETE", f"/api/delete/{entity_id}")

    @allure.step("Создать сущность")
    def create_entity(self, payload: EntityRequest) -> CreatedEntityResponse:
        response = self._create_entity_response(payload)
        return CreatedEntityResponse(id=int(response.text.strip()))

    @allure.step("Получить сущность по id={entity_id}")
    def get_entity(self, entity_id: int) -> EntityResponse:
        response = self._get_entity_response(entity_id)
        return EntityResponse.model_validate(response.json())

    @allure.step("Получить список сущностей")
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

        response = self._get_all_entities_response(params)
        return EntityListResponse.model_validate(response.json())

    @allure.step("Обновить сущность с id={entity_id}")
    def update_entity(self, entity_id: int, payload: EntityRequest) -> NoContentResponse:
        response = self._update_entity_response(entity_id, payload)
        return NoContentResponse(status_code=response.status_code)

    @allure.step("Удалить сущность с id={entity_id}")
    def delete_entity(self, entity_id: int) -> NoContentResponse:
        response = self._delete_entity_response(entity_id)
        return NoContentResponse(status_code=response.status_code)
