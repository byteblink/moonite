from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.models.mixins import BaseFieldsMixin


class Merchant(Base, BaseFieldsMixin):
    __tablename__ = "merchants"

    company_name: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="公司名")
    contact_name: Mapped[str] = mapped_column(String(128), nullable=False, server_default="", comment="联系人")
    contact_mobile: Mapped[str] = mapped_column(String(32), nullable=False, server_default="", comment="联系人手机号")
    company_type: Mapped[str] = mapped_column(String(32), nullable=False, server_default="", comment="公司类型（如自营、非自营等）")
