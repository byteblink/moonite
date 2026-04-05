from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ShopBase(BaseModel):
    merchant_id: int  # 所属商家ID
    shop_name: str = ""  # 店铺名
    contact_name: str = ""  # 联系人
    shop_type: str = ""  # 门店类型（自营/加盟/共享/品牌联营等）
    contact_phone: str = ""  # 联系人电话
    province: str = ""  # 省
    province_code: str = ""  # 省级行政区划代码
    city: str = ""  # 市
    city_code: str = ""  # 市级行政区划代码
    district: str = ""  # 区/县
    district_code: str = ""  # 区县级行政区划代码
    street: str = ""  # 街道
    street_code: str = ""  # 街道级区划代码
    address: str = ""  # 详细地址
    latitude: float | None = None  # 纬度
    longitude: float | None = None  # 经度
    geohash: str = ""  # 地理位置 geohash
    business_status: str = ""  # 营业状态（营业、歇业等）
    shop_images: list[str] = Field(default_factory=list)  # 店铺图片列表
    tags: list[str] = Field(default_factory=list)  # 标签列表
    description: str = ""  # 门店描述


class ShopCreate(ShopBase):
    pass


class ShopUpdate(BaseModel):
    merchant_id: int | None = None  # 所属商家ID
    shop_name: str | None = None  # 店铺名
    contact_name: str | None = None  # 联系人
    shop_type: str | None = None  # 门店类型（自营/加盟/共享/品牌联营等）
    contact_phone: str | None = None  # 联系人电话
    province: str | None = None  # 省
    province_code: str | None = None  # 省级行政区划代码
    city: str | None = None  # 市
    city_code: str | None = None  # 市级行政区划代码
    district: str | None = None  # 区/县
    district_code: str | None = None  # 区县级行政区划代码
    street: str | None = None  # 街道
    street_code: str | None = None  # 街道级区划代码
    address: str | None = None  # 详细地址
    latitude: float | None = None  # 纬度
    longitude: float | None = None  # 经度
    geohash: str | None = None  # 地理位置 geohash
    business_status: str | None = None  # 营业状态（营业、歇业等）
    shop_images: list[str] | None = None  # 店铺图片列表
    tags: list[str] | None = None  # 标签列表
    description: str | None = None  # 门店描述


class ShopOut(ShopBase):
    model_config = ConfigDict(from_attributes=True)

    id: int  # 主键，自增
    tenant_id: int  # 租户ID
    is_deleted: bool  # 是否删除
    created_at: datetime  # 创建时间，插入时自动赋值
    updated_at: datetime  # 更新时间，更新时自动赋值
    deleted_at: Optional[datetime] = None  # 删除时间（软删时记录）
