from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.models.mixins import BaseFieldsMixin


class Role(Base, BaseFieldsMixin):
    __tablename__ = "roles"

    role_name: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="角色名称")
    description: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="角色描述")
