from __future__ import annotations

from uuid import uuid4

from src.api_models import AdditionRequest, EntityRequest


DEFAULT_IMPORTANT_NUMBERS = [42, 87, 15]
DEFAULT_ADDITIONAL_NUMBER = 123
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10


def build_entity_request(
    *,
    title_prefix: str = "api-entity",
    verified: bool = True,
    additional_info: str = "Дополнительные сведения",
    additional_number: int = DEFAULT_ADDITIONAL_NUMBER,
    important_numbers: list[int] | None = None,
) -> EntityRequest:
    unique_suffix = uuid4().hex[:8]
    return EntityRequest(
        title=f"{title_prefix}-{unique_suffix}",
        verified=verified,
        addition=AdditionRequest(
            additional_info=additional_info,
            additional_number=additional_number,
        ),
        important_numbers=important_numbers or DEFAULT_IMPORTANT_NUMBERS,
    )
