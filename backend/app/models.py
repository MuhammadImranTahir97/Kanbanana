from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator


class Status(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


def _validate_title(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("Title is required.")
    if len(stripped) > 100:
        raise ValueError("Title must be 100 characters or less.")
    return stripped


def _validate_description(value: str) -> str:
    stripped = value.strip()
    if len(stripped) > 1000:
        raise ValueError("Description must be 1000 characters or less.")
    return stripped


class CardCreate(BaseModel):
    title: str
    description: str = ""

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        return _validate_title(value)

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        return _validate_description(value)


class CardUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        return _validate_title(value) if value is not None else None

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str | None) -> str | None:
        return _validate_description(value) if value is not None else None


class Card(BaseModel):
    id: int
    title: str
    description: str
    status: Status
    created_at: datetime
