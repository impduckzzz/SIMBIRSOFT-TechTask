from __future__ import annotations

import pytest

from config.api_test_data import build_entity_request
from src.api_client import EntityApiClient
from src.api_models import EntityRequest


@pytest.fixture(scope="session")
def api_client() -> EntityApiClient:
    return EntityApiClient()


@pytest.fixture(scope="session")
def entity_request_factory():
    def _factory(**kwargs) -> EntityRequest:
        return build_entity_request(**kwargs)

    return _factory


@pytest.fixture()
def created_entity_factory(api_client: EntityApiClient):
    created_entity_ids: list[int] = []

    def _factory(payload: EntityRequest):
        created = api_client.create_entity(payload)
        created_entity_ids.append(created.id)
        return created

    yield _factory

    for entity_id in created_entity_ids:
        try:
            api_client.delete_entity(entity_id)
        except AssertionError:
            pass


@pytest.fixture()
def created_entity(entity_request_factory, created_entity_factory):
    payload = entity_request_factory()
    created = created_entity_factory(payload)
    return payload, created
