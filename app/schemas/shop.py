from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ShopBase(BaseModel):
    merchant_id: int
    shop_name: str = ""
    contact_name: str = ""
    shop_type: str = ""
    contact_phone: str = ""
    province: str = ""
    province_code: str = ""
    city: str = ""
    city_code: str = ""
    district: str = ""
    district_code: str = ""
    street: str = ""
    street_code: str = ""
    address: str = ""
    latitude: float | None = None
    longitude: float | None = None
    geohash: str = ""
    business_status: str = ""
    shop_images: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    description: str = ""


class ShopCreate(ShopBase):
    pass


class ShopUpdate(BaseModel):
    merchant_id: int | None = None
    shop_name: str | None = None
    contact_name: str | None = None
    shop_type: str | None = None
    contact_phone: str | None = None
    province: str | None = None
    province_code: str | None = None
    city: str | None = None
    city_code: str | None = None
    district: str | None = None
    district_code: str | None = None
    street: str | None = None
    street_code: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    geohash: str | None = None
    business_status: str | None = None
    shop_images: list[str] | None = None
    tags: list[str] | None = None
    description: str | None = None


class ShopOut(ShopBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
