from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Identity, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class OrderDiscount(Base):
    __tablename__ = "order_discounts"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    order_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("room_orders.id", ondelete="SET NULL"), nullable=True
    )
    discount_type: Mapped[str] = mapped_column(String(8), nullable=False, server_default="")
    discount_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    coupon_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    external_platform: Mapped[str] = mapped_column(String(16), nullable=False, server_default="")
    discount_reason: Mapped[str] = mapped_column(String(200), nullable=False, server_default="")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
