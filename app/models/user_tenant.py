from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.models.mixins import BaseFieldsMixin, TenantMixin


class UserTenant(Base, BaseFieldsMixin, TenantMixin):
    __tablename__ = "user_tenants"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, comment="用户ID")
