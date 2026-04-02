from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EmployeeRoleBase(BaseModel):
    employee_id: int
    role_id: int
    shop_id: int | None = None


class EmployeeRoleCreate(EmployeeRoleBase):
    pass


class EmployeeRoleUpdate(BaseModel):
    employee_id: int | None = None
    role_id: int | None = None
    shop_id: int | None = None


class EmployeeRoleOut(EmployeeRoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
