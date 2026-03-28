from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RoomBase(BaseModel):
    shop_id: int
    room_name: str = ""
    room_type: str = ""
    room_area: Decimal | None = None
    capacity: int | None = None
    base_price: Decimal | None = None
    renew_price: Decimal | None = None
    room_status: str = ""
    room_images: list[str] = Field(default_factory=list)
    description: str = ""


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    shop_id: int | None = None
    room_name: str | None = None
    room_type: str | None = None
    room_area: Decimal | None = None
    capacity: int | None = None
    base_price: Decimal | None = None
    renew_price: Decimal | None = None
    room_status: str | None = None
    room_images: list[str] | None = None
    description: str | None = None


class RoomOut(RoomBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
