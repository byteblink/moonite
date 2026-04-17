from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RoomBase(BaseModel):
    shop_id: int  # 所属店铺ID
    room_name: str = ""  # 房间名
    room_type: str = ""  # 房间类型（办公/会议/休息等）
    room_area: Decimal | None = None  # 房间面积
    capacity: int | None = None  # 容量（适用人数）
    base_price: Decimal | None = None  # 房间 1 小时单价
    renew_price: Decimal | None = None  # 续单 1 小时单价
    room_status: str = ""  # 房间状态（空闲/占用/维修/下线/预订等）
    room_images: list[str] = Field(default_factory=list)  # 房间图片列表
    description: str = ""  # 房间描述


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    shop_id: int | None = None  # 所属店铺ID
    room_name: str | None = None  # 房间名
    room_type: str | None = None  # 房间类型（办公/会议/休息等）
    room_area: Decimal | None = None  # 房间面积
    capacity: int | None = None  # 容量（适用人数）
    base_price: Decimal | None = None  # 房间 1 小时单价
    renew_price: Decimal | None = None  # 续单 1 小时单价
    room_status: str | None = None  # 房间状态（空闲/占用/维修/下线/预订等）
    room_images: list[str] | None = None  # 房间图片列表
    description: str | None = None  # 房间描述


class RoomOut(RoomBase):
    model_config = ConfigDict(from_attributes=True)

    id: int  # 主键，自增
    is_deleted: bool  # 是否删除
    created_at: datetime  # 创建时间，插入时自动赋值
    updated_at: datetime  # 更新时间，更新时自动赋值
    deleted_at: Optional[datetime] = None  # 删除时间（软删时记录）
