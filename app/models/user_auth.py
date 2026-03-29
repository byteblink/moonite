from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Identity, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserAuth(Base):
    __tablename__ = "user_auths"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    platform: Mapped[str] = mapped_column(String(16), nullable=False, server_default="")
    openid: Mapped[str] = mapped_column(String(128), nullable=False, server_default="")
    unionid: Mapped[str] = mapped_column(String(128), nullable=False, server_default="")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
