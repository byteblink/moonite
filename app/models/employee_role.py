from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.models.mixins import BaseFieldsMixin


class EmployeeRole(Base, BaseFieldsMixin):
    __tablename__ = "employee_roles"

    employee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("employees.id", ondelete="RESTRICT"), nullable=False, comment="员工ID")
    role_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False, comment="角色ID")
    shop_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="可选：不同角色在不同门店生效")
