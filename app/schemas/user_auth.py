from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserAuthBase(BaseModel):
    user_id: int  # 用户ID
    platform: str = ""  # 平台（wechat/douyin/kuaishou 等）
    openid: str = ""  # 平台 openid
    unionid: str = ""  # 平台 unionid


class UserAuthCreate(UserAuthBase):
    pass


class UserAuthUpdate(BaseModel):
    user_id: int | None = None  # 用户ID
    platform: str | None = None  # 平台（wechat/douyin/kuaishou 等）
    openid: str | None = None  # 平台 openid
    unionid: str | None = None  # 平台 unionid


class UserAuthOut(UserAuthBase):
    model_config = ConfigDict(from_attributes=True)

    id: int  # 主键，自增
    is_deleted: bool  # 是否删除
    created_at: datetime  # 创建时间，插入时自动赋值
    updated_at: datetime  # 更新时间，更新时自动赋值
    deleted_at: Optional[datetime] = None  # 删除时间（软删时记录）
