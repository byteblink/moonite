from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TenantBase(BaseModel):
    tenant_name: str = ""
    code: str = ""


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    tenant_name: str | None = None
    code: str | None = None


class TenantOut(TenantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
