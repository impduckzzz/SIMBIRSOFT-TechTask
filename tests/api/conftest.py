from __future__ import annotations

import pytest

from config.api_test_data import build_entity_request
from src.api_client import EntityApiClient
from src.api_models import EntityRequest


@pytest.fixture()
def api_client() -> EntityApiClient:
    return EntityApiClient()


@pytest.fixture()
def entity_request_factory():
    def _factory(**kwargs) -> EntityRequest:
        return build_entity_request(**kwargs)

    return _factory


@pytest.fixture()
def created_entity(api_client: EntityApiClient, entity_request_factory):
    payload = entity_request_factory()
    created = api_client.create_entity(payload)
    yield payload, created
    try:
        api_client.delete_entity(created.id)
    except AssertionError:
        pass
