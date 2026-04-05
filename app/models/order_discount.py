from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.models.mixins import BaseFieldsMixin


class OrderDiscount(Base, BaseFieldsMixin):
    __tablename__ = "order_discounts"

    order_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("room_orders.id", ondelete="SET NULL"), nullable=True, comment="订单ID"
    )
    discount_type: Mapped[str] = mapped_column(String(8), nullable=False, server_default="", comment="优惠类型：balance/coupon/group/external")
    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="优惠金额")
    coupon_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, comment="优惠券ID")
    external_platform: Mapped[str] = mapped_column(String(16), nullable=False, server_default="", comment="外部券平台：meituan/douyin 等")
    discount_reason: Mapped[str] = mapped_column(String(200), nullable=False, server_default="", comment="优惠原因")
