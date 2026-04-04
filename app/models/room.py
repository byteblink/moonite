from decimal import Decimal
from typing import Optional

from sqlalchemy import ARRAY, BigInteger, ForeignKey, Integer, Numeric, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import BaseFieldsMixin, TenantMixin


class Room(Base, BaseFieldsMixin, TenantMixin):
    __tablename__ = "rooms"

    shop_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("shops.id", ondelete="RESTRICT"), nullable=False, comment="所属店铺ID"
    )
    room_name: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="房间名")
    room_type: Mapped[str] = mapped_column(String(32), nullable=False, server_default="", comment="房间类型（办公/会议/休息等）")
    room_area: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True, comment="房间面积")
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="容量（适用人数）")
    base_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="房间 1 小时单价")
    renew_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="续单 1 小时单价")
    room_status: Mapped[str] = mapped_column(String(16), nullable=False, server_default="", comment="房间状态（空闲/占用/维修/下线/预订等）")
    room_images: Mapped[list[str]] = mapped_column(
        ARRAY(Text), nullable=False, server_default=text("ARRAY[]::text[]"), comment="房间图片列表"
    )
    description: Mapped[str] = mapped_column(Text, nullable=False, server_default="", comment="房间描述")
