from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MerchantBase(BaseModel):
    tenant_id: int
    company_name: str = ""  # 公司名
    contact_name: str = ""  # 联系人
    contact_mobile: str = ""  # 联系人手机号
    company_type: str = ""  # 公司类型（如自营、非自营等）


class MerchantCreate(MerchantBase):
    pass


class MerchantUpdate(BaseModel):
    tenant_id: int | None = None
    company_name: str | None = None  # 公司名
    contact_name: str | None = None  # 联系人
    contact_mobile: str | None = None  # 联系人手机号
    company_type: str | None = None  # 公司类型（如自营、非自营等）


class MerchantOut(MerchantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int  # 主键，自增
    is_deleted: bool  # 是否删除
    created_at: datetime  # 创建时间，插入时自动赋值
    updated_at: datetime  # 更新时间，更新时自动赋值
    deleted_at: Optional[datetime] = None  # 删除时间（软删时记录）
