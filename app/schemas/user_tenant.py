from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserTenantBase(BaseModel):
    tenant_id: int
    user_id: int


class UserTenantCreate(UserTenantBase):
    pass


class UserTenantUpdate(BaseModel):
    tenant_id: int | None = None
    user_id: int | None = None


class UserTenantOut(UserTenantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
