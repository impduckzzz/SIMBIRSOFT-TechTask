from __future__ import annotations

from pydantic import BaseModel, Field


class AdditionRequest(BaseModel):
    additional_info: str | None = None
    additional_number: int | None = None


class EntityRequest(BaseModel):
    title: str
    verified: bool
    addition: AdditionRequest | None = None
    important_numbers: list[int] = Field(default_factory=list)


class AdditionResponse(BaseModel):
    id: int | None = None
    additional_info: str | None = None
    additional_number: int | None = None


class EntityResponse(BaseModel):
    id: int
    title: str
    verified: bool
    addition: AdditionResponse | None = None
    important_numbers: list[int] = Field(default_factory=list)


class EntityListResponse(BaseModel):
    entity: list[EntityResponse]
    page: int | None = None
    perPage: int | None = None


class CreatedEntityResponse(BaseModel):
    id: int


class NoContentResponse(BaseModel):
    status_code: int
