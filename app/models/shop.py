from datetime import datetime
from typing import Optional

from sqlalchemy import ARRAY, BigInteger, Boolean, DateTime, Float, ForeignKey, Identity, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Shop(Base):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True, comment="主键，自增")
    tenant_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False, comment="租户ID")
    merchant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("merchants.id", ondelete="RESTRICT"), nullable=False, comment="所属商家ID"
    )
    shop_name: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="店铺名")
    contact_name: Mapped[str] = mapped_column(String(128), nullable=False, server_default="", comment="联系人")
    shop_type: Mapped[str] = mapped_column(String(32), nullable=False, server_default="", comment="门店类型（自营/加盟/共享/品牌联营等）")
    contact_phone: Mapped[str] = mapped_column(String(32), nullable=False, server_default="", comment="联系人电话")
    province: Mapped[str] = mapped_column(String(64), nullable=False, server_default="", comment="省")
    province_code: Mapped[str] = mapped_column(String(16), nullable=False, server_default="", comment="省级行政区划代码")
    city: Mapped[str] = mapped_column(String(64), nullable=False, server_default="", comment="市")
    city_code: Mapped[str] = mapped_column(String(16), nullable=False, server_default="", comment="市级行政区划代码")
    district: Mapped[str] = mapped_column(String(64), nullable=False, server_default="", comment="区/县")
    district_code: Mapped[str] = mapped_column(String(16), nullable=False, server_default="", comment="区县级行政区划代码")
    street: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="街道")
    street_code: Mapped[str] = mapped_column(String(16), nullable=False, server_default="", comment="街道级区划代码")
    address: Mapped[str] = mapped_column(String(255), nullable=False, server_default="", comment="详细地址")
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="纬度")
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="经度")
    geohash: Mapped[str] = mapped_column(String(32), nullable=False, server_default="", comment="地理位置 geohash")
    business_status: Mapped[str] = mapped_column(String(16), nullable=False, server_default="", comment="营业状态（营业、歇业等）")
    shop_images: Mapped[list[str]] = mapped_column(
        ARRAY(Text), nullable=False, server_default=text("ARRAY[]::text[]"), comment="店铺图片列表"
    )
    tags: Mapped[list[str]] = mapped_column(
        ARRAY(Text), nullable=False, server_default=text("ARRAY[]::text[]"), comment="标签列表"
    )
    description: Mapped[str] = mapped_column(Text, nullable=False, server_default="", comment="门店描述")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false", comment="是否删除")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="删除时间（软删时记录）")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="创建时间，插入时自动赋值"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="更新时间，更新时自动赋值"
    )
