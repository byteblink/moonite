from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    password: str = ""
    email: str = ""
    username: str = ""
    mobile: str = ""  # 手机号
    nickname: str = ""  # 昵称
    avatar: str = ""  # 头像 URL
    gender: int = 0  # 性别：0 未知，1 男，2 女
    birthday: Optional[date] = None  # 生日


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    password: str | None = None
    email: str | None = None
    username: str | None = None
    mobile: str | None = None  # 手机号
    nickname: str | None = None  # 昵称
    avatar: str | None = None  # 头像 URL
    gender: int | None = None  # 性别：0 未知，1 男，2 女
    birthday: Optional[date] = None  # 生日


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int  # 主键，自增
    is_deleted: bool  # 是否删除
    created_at: datetime  # 创建时间，插入时自动赋值
    updated_at: datetime  # 更新时间，更新时自动赋值
    deleted_at: Optional[datetime] = None  # 删除时间（软删时记录）
