from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Identity, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class OrderDiscount(Base):
    __tablename__ = "order_discounts"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True, comment="主键，自增")
    order_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("room_orders.id", ondelete="SET NULL"), nullable=True, comment="订单ID"
    )
    discount_type: Mapped[str] = mapped_column(String(8), nullable=False, server_default="", comment="优惠类型：balance/coupon/group/external")
    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="优惠金额")
    coupon_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, comment="优惠券ID")
    external_platform: Mapped[str] = mapped_column(String(16), nullable=False, server_default="", comment="外部券平台：meituan/douyin 等")
    discount_reason: Mapped[str] = mapped_column(String(200), nullable=False, server_default="", comment="优惠原因")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false", comment="是否删除")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="删除时间（软删时记录）")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="创建时间，插入时自动赋值"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="更新时间，更新时自动赋值"
    )
