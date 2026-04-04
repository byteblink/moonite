from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, Identity, text
from sqlalchemy.orm import Mapped, mapped_column


class BaseFieldsMixin:
    """
    通用基础字段：
    - id: 主键自增
    - is_deleted: 软删除标记
    - deleted_at: 软删除时间
    - created_at: 创建时间
    - updated_at: 更新时间
    """

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True,
        comment="主键ID",
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
        comment="是否删除",
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="删除时间（软删时记录）",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        comment="创建时间",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        comment="更新时间",
    )

    def soft_delete(self) -> None:
        """软删除"""
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        """恢复"""
        self.is_deleted = False
        self.deleted_at = None