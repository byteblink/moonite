from datetime import date, datetime
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, Boolean, Date, DateTime, Identity, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True, comment="主键，自增")
    tenant_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False, comment="租户ID")
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, comment="用户ID")
    shop_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("shops.id", ondelete="RESTRICT"), nullable=False, comment="店铺ID")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false", comment="是否删除")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="删除时间（软删时记录）")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="创建时间，插入时自动赋值"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="更新时间，更新时自动赋值"
    )
