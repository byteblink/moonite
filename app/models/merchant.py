from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, Identity, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True, comment="主键，自增")
    company_name: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="公司名")
    contact_name: Mapped[str] = mapped_column(String(128), nullable=False, server_default="", comment="联系人")
    contact_mobile: Mapped[str] = mapped_column(String(32), nullable=False, server_default="", comment="联系人手机号")
    company_type: Mapped[str] = mapped_column(String(32), nullable=False, server_default="", comment="公司类型（如自营、非自营等）")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false", comment="是否删除")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="删除时间（软删时记录）")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="创建时间，插入时自动赋值"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="更新时间，更新时自动赋值"
    )
