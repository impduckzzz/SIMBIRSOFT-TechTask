from __future__ import annotations

import allure
import pytest

from config.api_test_data import DEFAULT_PAGE, DEFAULT_PER_PAGE
from src.api_client import EntityApiClient
from src.api_models import CreatedEntityResponse, EntityRequest


@allure.epic("API-сервис сущностей")
@allure.feature("Сущности")
@pytest.mark.api
@allure.story("Создание сущности")
@allure.title("Можно создать новую сущность")
@allure.description("Проверка создания новой сущности и последующего чтения созданных данных.")
def test_create_entity(api_client: EntityApiClient, entity_request_factory):
    payload = entity_request_factory(title_prefix="create-entity")

    with allure.step("Создать новую сущность"):
        created_entity = api_client.create_entity(payload)

    try:
        with allure.step("Получить созданную сущность и проверить её поля"):
            actual_entity = api_client.get_entity(created_entity.id)
            assert created_entity.id > 0
            assert actual_entity.title == payload.title
            assert actual_entity.verified is payload.verified
            assert actual_entity.important_numbers == payload.important_numbers
            assert actual_entity.addition is not None
            assert actual_entity.addition.additional_info == payload.addition.additional_info
            assert actual_entity.addition.additional_number == payload.addition.additional_number
    finally:
        api_client.delete_entity(created_entity.id)


@allure.epic("API-сервис сущностей")
@allure.feature("Сущности")
@pytest.mark.api
@allure.story("Получение сущности")
@allure.title("Можно получить сущность по идентификатору")
@allure.description("Проверка получения ранее созданной сущности по её идентификатору.")
def test_get_entity_by_id(
    api_client: EntityApiClient,
    created_entity: tuple[EntityRequest, CreatedEntityResponse],
):
    payload, created = created_entity

    with allure.step("Запросить сущность по идентификатору"):
        actual_entity = api_client.get_entity(created.id)

    with allure.step("Проверить состав и значения полей полученной сущности"):
        assert actual_entity.id == created.id
        assert actual_entity.title == payload.title
        assert actual_entity.verified is payload.verified
        assert actual_entity.important_numbers == payload.important_numbers
        assert actual_entity.addition is not None
        assert actual_entity.addition.additional_info == payload.addition.additional_info
        assert actual_entity.addition.additional_number == payload.addition.additional_number


@allure.epic("API-сервис сущностей")
@allure.feature("Сущности")
@pytest.mark.api
@allure.story("Получение списка сущностей")
@allure.title("Можно получить список сущностей с фильтрацией и пагинацией")
@allure.description("Проверка получения списка сущностей с фильтрацией по полям и параметрами пагинации.")
def test_get_all_entities(
    api_client: EntityApiClient,
    created_entity: tuple[EntityRequest, CreatedEntityResponse],
):
    payload, created = created_entity

    with allure.step("Запросить список сущностей с фильтрацией и пагинацией"):
        entities = api_client.get_all_entities(
            title=payload.title,
            verified=payload.verified,
            page=DEFAULT_PAGE,
            per_page=DEFAULT_PER_PAGE,
        )

    with allure.step("Найти созданную сущность в ответе и проверить её поля"):
        matched_entity = next(entity for entity in entities.entity if entity.id == created.id)
        assert entities.page == DEFAULT_PAGE
        assert entities.perPage == DEFAULT_PER_PAGE
        assert matched_entity.title == payload.title
        assert matched_entity.verified is payload.verified
        assert matched_entity.important_numbers == payload.important_numbers
        assert matched_entity.addition is not None
        assert matched_entity.addition.additional_info == payload.addition.additional_info
        assert matched_entity.addition.additional_number == payload.addition.additional_number


@allure.epic("API-сервис сущностей")
@allure.feature("Сущности")
@pytest.mark.api
@allure.story("Обновление сущности")
@allure.title("Можно обновить существующую сущность")
@allure.description("Проверка обновления полей сущности и чтения актуальных данных после изменения.")
def test_update_entity(
    api_client: EntityApiClient,
    created_entity: tuple[EntityRequest, CreatedEntityResponse],
    entity_request_factory,
):
    _, created = created_entity
    updated_payload = entity_request_factory(
        title_prefix="updated-entity",
        verified=False,
        additional_info="Обновлённые сведения",
        additional_number=456,
        important_numbers=[7, 8, 9],
    )

    with allure.step("Обновить существующую сущность"):
        update_result = api_client.update_entity(created.id, updated_payload)

    with allure.step("Получить обновлённую сущность и проверить её поля"):
        actual_entity = api_client.get_entity(created.id)
        assert update_result.status_code == 204
        assert actual_entity.id == created.id
        assert actual_entity.title == updated_payload.title
        assert actual_entity.verified is updated_payload.verified
        assert actual_entity.important_numbers == updated_payload.important_numbers
        assert actual_entity.addition is not None
        assert actual_entity.addition.additional_info == updated_payload.addition.additional_info
        assert actual_entity.addition.additional_number == updated_payload.addition.additional_number


@allure.epic("API-сервис сущностей")
@allure.feature("Сущности")
@pytest.mark.api
@allure.story("Удаление сущности")
@allure.title("Можно удалить существующую сущность")
@allure.description("Проверка удаления сущности и отсутствия удалённой записи в общем списке.")
def test_delete_entity(
    api_client: EntityApiClient,
    created_entity: tuple[EntityRequest, CreatedEntityResponse],
):
    _, created = created_entity

    with allure.step("Удалить сущность по идентификатору"):
        delete_result = api_client.delete_entity(created.id)

    with allure.step("Получить список сущностей и убедиться, что удалённой записи больше нет"):
        entities = api_client.get_all_entities()
        assert delete_result.status_code == 204
        assert all(entity.id != created.id for entity in entities.entity)
