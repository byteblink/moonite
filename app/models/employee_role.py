from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, Boolean, DateTime, Identity, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class EmployeeRole(Base):
    __tablename__ = "employee_roles"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True, comment="主键，自增")
    employee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("employees.id", ondelete="RESTRICT"), nullable=False, comment="员工ID")
    role_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False, comment="角色ID")
    shop_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="可选：不同角色在不同门店生效")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false", comment="是否删除")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="删除时间（软删时记录）")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="创建时间，插入时自动赋值"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="更新时间，更新时自动赋值"
    )
