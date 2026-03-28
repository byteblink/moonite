from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, Identity, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False, server_default="")
    contact_name: Mapped[str] = mapped_column(String(128), nullable=False, server_default="")
    contact_mobile: Mapped[str] = mapped_column(String(32), nullable=False, server_default="")
    company_type: Mapped[str] = mapped_column(String(32), nullable=False, server_default="")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
