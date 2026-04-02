from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderDiscountBase(BaseModel):
    order_id: int | None = None  # 订单ID
    discount_type: str = ""  # 优惠类型：balance/coupon/group/external
    discount_amount: Decimal | None = None  # 优惠金额
    coupon_id: int | None = None  # 优惠券ID
    external_platform: str = ""  # 外部券平台：meituan/douyin 等
    discount_reason: str = ""  # 优惠原因


class OrderDiscountCreate(OrderDiscountBase):
    pass


class OrderDiscountUpdate(BaseModel):
    order_id: int | None = None  # 订单ID
    discount_type: str | None = None  # 优惠类型：balance/coupon/group/external
    discount_amount: Decimal | None = None  # 优惠金额
    coupon_id: int | None = None  # 优惠券ID
    external_platform: str | None = None  # 外部券平台：meituan/douyin 等
    discount_reason: str | None = None  # 优惠原因


class OrderDiscountOut(OrderDiscountBase):
    model_config = ConfigDict(from_attributes=True)

    id: int  # 主键，自增
    is_deleted: bool  # 是否删除
    created_at: datetime  # 创建时间，插入时自动赋值
    updated_at: datetime  # 更新时间，更新时自动赋值
    deleted_at: Optional[datetime] = None  # 删除时间（软删时记录）
