from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EmployeeBase(BaseModel):
    tenant_id: int
    user_id: int
    is_active: bool = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    tenant_id: int | None = None
    user_id: int | None = None
    is_active: bool | None = None


class EmployeeOut(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
