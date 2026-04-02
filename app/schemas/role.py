from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    role_name: str = ""
    description: str = ""


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    role_name: str | None = None
    description: str | None = None


class RoleOut(RoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
