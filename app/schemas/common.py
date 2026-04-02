from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Paginated(BaseModel, Generic[T]):
    items: list[T]
    total: int
    skip: int = Field(ge=0)
    limit: int = Field(ge=1, le=200)


class Envelope(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: T | None = None
    timestamp: int
    request_id: str
