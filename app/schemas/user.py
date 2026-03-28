from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    mobile: str = ""
    nickname: str = ""
    avatar: str = ""
    gender: int = 0
    birthday: Optional[date] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    mobile: str | None = None
    nickname: str | None = None
    avatar: str | None = None
    gender: int | None = None
    birthday: Optional[date] = None


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
