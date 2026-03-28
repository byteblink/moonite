from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MerchantBase(BaseModel):
    company_name: str = ""
    contact_name: str = ""
    contact_mobile: str = ""
    company_type: str = ""


class MerchantCreate(MerchantBase):
    pass


class MerchantUpdate(BaseModel):
    company_name: str | None = None
    contact_name: str | None = None
    contact_mobile: str | None = None
    company_type: str | None = None


class MerchantOut(MerchantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
