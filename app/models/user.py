from datetime import date
from typing import Optional

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.models.mixins import BaseFieldsMixin


class User(Base, BaseFieldsMixin):
    __tablename__ = "users"

    mobile: Mapped[str] = mapped_column(String(32), nullable=False, server_default="", comment="手机号")
    password: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="密码")
    email: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="邮箱")
    username: Mapped[str] = mapped_column(String(128), nullable=False, server_default="", comment="用户名")
    nickname: Mapped[str] = mapped_column(String(128), nullable=False, server_default="", comment="昵称")
    avatar: Mapped[str] = mapped_column(String(512), nullable=False, server_default="", comment="头像 URL")
    gender: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0", comment="性别：0 未知，1 男，2 女")
    birthday: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="生日")
