from datetime import date, datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Identity, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True, comment="主键，自增")
    mobile: Mapped[str] = mapped_column(String(32), nullable=False, server_default="", comment="手机号")
    nickname: Mapped[str] = mapped_column(String(128), nullable=False, server_default="", comment="昵称")
    avatar: Mapped[str] = mapped_column(String(512), nullable=False, server_default="", comment="头像 URL")
    gender: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0", comment="性别：0 未知，1 男，2 女")
    birthday: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="生日")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false", comment="是否删除")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="删除时间（软删时记录）")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="创建时间，插入时自动赋值"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="更新时间，更新时自动赋值"
    )
