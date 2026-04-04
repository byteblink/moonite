from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import BaseFieldsMixin


class Tenant(Base, BaseFieldsMixin):
    __tablename__ = "tenants"

    tenant_name: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="租户名称")
    code: Mapped[str] = mapped_column(String(128), nullable=False, server_default="", comment="租户唯一标识")
