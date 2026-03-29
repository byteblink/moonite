from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Identity, Integer, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class RoomOrder(Base):
    __tablename__ = "room_orders"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    order_number: Mapped[str] = mapped_column(String(50), nullable=False)
    ref_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("room_orders.id", ondelete="SET NULL"), nullable=True
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    shop_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("shops.id", ondelete="SET NULL"), nullable=True
    )
    room_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True
    )
    order_type: Mapped[str] = mapped_column(String(8), nullable=False, server_default="")
    source_platform: Mapped[str] = mapped_column(String(8), nullable=False, server_default="")
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_minute: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    order_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    renew_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    package_name: Mapped[str] = mapped_column(String(50), nullable=False, server_default="")
    package_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    package_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    total_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    pay_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    order_status: Mapped[str] = mapped_column(String(8), nullable=False, server_default="created")
    remark: Mapped[str] = mapped_column(String(200), nullable=False, server_default="")
    pay_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    finish_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cancel_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    refund_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    pay_channel: Mapped[str] = mapped_column(String(4), nullable=False, server_default="")
    refund_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
