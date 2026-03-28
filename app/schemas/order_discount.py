from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderDiscountBase(BaseModel):
    order_id: int | None = None
    discount_type: str = ""
    discount_amount: Decimal | None = None
    coupon_id: int | None = None
    external_platform: str = ""
    discount_reason: str = ""


class OrderDiscountCreate(OrderDiscountBase):
    pass


class OrderDiscountUpdate(BaseModel):
    order_id: int | None = None
    discount_type: str | None = None
    discount_amount: Decimal | None = None
    coupon_id: int | None = None
    external_platform: str | None = None
    discount_reason: str | None = None


class OrderDiscountOut(OrderDiscountBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
