from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import ARRAY, BigInteger, Boolean, DateTime, ForeignKey, Identity, Integer, Numeric, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    shop_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("shops.id", ondelete="RESTRICT"), nullable=False
    )
    room_name: Mapped[str] = mapped_column(String(255), nullable=False, server_default="")
    room_type: Mapped[str] = mapped_column(String(32), nullable=False, server_default="")
    room_area: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    base_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    renew_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    room_status: Mapped[str] = mapped_column(String(16), nullable=False, server_default="")
    room_images: Mapped[list[str]] = mapped_column(
        ARRAY(Text), nullable=False, server_default=text("ARRAY[]::text[]")
    )
    description: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
