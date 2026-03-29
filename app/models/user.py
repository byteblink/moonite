from datetime import date, datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Identity, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    mobile: Mapped[str] = mapped_column(String(32), nullable=False, server_default="")
    nickname: Mapped[str] = mapped_column(String(128), nullable=False, server_default="")
    avatar: Mapped[str] = mapped_column(String(512), nullable=False, server_default="")
    gender: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    birthday: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
