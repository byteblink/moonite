from datetime import date, datetime
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, Boolean, Date, DateTime, Identity, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserToken(Base):
    __tablename__ = "user_tokens"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True, comment="主键，自增")
    tenant_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False, comment="租户ID")
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, comment="用户ID")
    login_type: Mapped[str] = mapped_column(String(16), nullable=False, server_default="", comment="登录类型（password/sms/wechat/douyin/kuaishou 等）")
    jti: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="jti")
    refresh_token_hash: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="refresh_token_hash")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="过期时间")
    platform: Mapped[str] = mapped_column(String(16), nullable=False, server_default="", comment="平台（wechat/douyin/kuaishou 等）")
    user_agent: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="用户代理")
    ip: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="IP地址")
    is_revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false", comment="是否已撤销")
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="撤销时间")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false", comment="是否删除")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="删除时间（软删时记录）")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="创建时间，插入时自动赋值"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="更新时间，更新时自动赋值"
    )
