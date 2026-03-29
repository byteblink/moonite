from datetime import datetime
from typing import Optional

from sqlalchemy import ARRAY, BigInteger, Boolean, DateTime, Float, ForeignKey, Identity, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Shop(Base):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    merchant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("merchants.id", ondelete="RESTRICT"), nullable=False
    )
    shop_name: Mapped[str] = mapped_column(String(255), nullable=False, server_default="")
    contact_name: Mapped[str] = mapped_column(String(128), nullable=False, server_default="")
    shop_type: Mapped[str] = mapped_column(String(32), nullable=False, server_default="")
    contact_phone: Mapped[str] = mapped_column(String(32), nullable=False, server_default="")
    province: Mapped[str] = mapped_column(String(64), nullable=False, server_default="")
    province_code: Mapped[str] = mapped_column(String(16), nullable=False, server_default="")
    city: Mapped[str] = mapped_column(String(64), nullable=False, server_default="")
    city_code: Mapped[str] = mapped_column(String(16), nullable=False, server_default="")
    district: Mapped[str] = mapped_column(String(64), nullable=False, server_default="")
    district_code: Mapped[str] = mapped_column(String(16), nullable=False, server_default="")
    street: Mapped[str] = mapped_column(String(255), nullable=False, server_default="")
    street_code: Mapped[str] = mapped_column(String(16), nullable=False, server_default="")
    address: Mapped[str] = mapped_column(String(255), nullable=False, server_default="")
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    geohash: Mapped[str] = mapped_column(String(32), nullable=False, server_default="")
    business_status: Mapped[str] = mapped_column(String(16), nullable=False, server_default="")
    shop_images: Mapped[list[str]] = mapped_column(
        ARRAY(Text), nullable=False, server_default=text("ARRAY[]::text[]")
    )
    tags: Mapped[list[str]] = mapped_column(
        ARRAY(Text), nullable=False, server_default=text("ARRAY[]::text[]")
    )
    description: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
