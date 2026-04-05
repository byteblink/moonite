from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.models.mixins import BaseFieldsMixin


class UserAuth(Base, BaseFieldsMixin):
    __tablename__ = "user_auths"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, comment="用户ID"
    )
    platform: Mapped[str] = mapped_column(String(16), nullable=False, server_default="", comment="平台（wechat/douyin/kuaishou 等）")
    openid: Mapped[str] = mapped_column(String(128), nullable=False, server_default="", comment="平台 openid")
    unionid: Mapped[str] = mapped_column(String(128), nullable=False, server_default="", comment="平台 unionid")
