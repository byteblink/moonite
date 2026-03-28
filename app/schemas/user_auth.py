from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserAuthBase(BaseModel):
    user_id: int
    platform: str = ""
    openid: str = ""
    unionid: str = ""


class UserAuthCreate(UserAuthBase):
    pass


class UserAuthUpdate(BaseModel):
    user_id: int | None = None
    platform: str | None = None
    openid: str | None = None
    unionid: str | None = None


class UserAuthOut(UserAuthBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
