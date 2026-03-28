from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RoomOrderBase(BaseModel):
    order_number: str
    ref_id: int | None = None
    user_id: int | None = None
    shop_id: int | None = None
    room_id: int | None = None
    order_type: str = ""
    source_platform: str = ""
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration_minute: int = 0
    order_price: Decimal | None = None
    renew_price: Decimal | None = None
    package_name: str = ""
    package_price: Decimal | None = None
    package_id: int | None = None
    total_price: Decimal | None = None
    pay_amount: Decimal | None = None
    order_status: str = "created"
    remark: str = ""
    pay_time: datetime | None = None
    finish_time: datetime | None = None
    cancel_time: datetime | None = None
    refund_time: datetime | None = None
    pay_channel: str = ""
    refund_amount: Decimal | None = None


class RoomOrderCreate(RoomOrderBase):
    pass


class RoomOrderUpdate(BaseModel):
    order_number: str | None = None
    ref_id: int | None = None
    user_id: int | None = None
    shop_id: int | None = None
    room_id: int | None = None
    order_type: str | None = None
    source_platform: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration_minute: int | None = None
    order_price: Decimal | None = None
    renew_price: Decimal | None = None
    package_name: str | None = None
    package_price: Decimal | None = None
    package_id: int | None = None
    total_price: Decimal | None = None
    pay_amount: Decimal | None = None
    order_status: str | None = None
    remark: str | None = None
    pay_time: datetime | None = None
    finish_time: datetime | None = None
    cancel_time: datetime | None = None
    refund_time: datetime | None = None
    pay_channel: str | None = None
    refund_amount: Decimal | None = None


class RoomOrderOut(RoomOrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
