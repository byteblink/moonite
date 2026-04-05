from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RoomOrderBase(BaseModel):
    order_number: str  # 生成的订单号
    ref_id: int | None = None  # 续单时为主订单主键ID，新单为 null
    user_id: int | None = None  # 下单人ID
    shop_id: int | None = None  # 门店ID
    room_id: int | None = None  # 房间ID
    order_type: str = ""  # 订单类型：package/hourly
    source_platform: str = ""  # 来源平台
    start_time: datetime | None = None  # 开始时间
    end_time: datetime | None = None  # 结束时间
    duration_minute: int = 0  # 总时长，单位分钟
    order_price: Decimal | None = None  # 房间单价
    renew_price: Decimal | None = None  # 续单单价
    package_name: str = ""  # 套餐名称
    package_price: Decimal | None = None  # 套餐总价
    package_price: Decimal | None = None  # 套餐总价
    package_id: int | None = None  # 套餐ID
    total_price: Decimal | None = None  # 总价
    pay_amount: Decimal | None = None  # 实际付款金额
    order_status: str = "created"  # 订单状态：created/paid/finished/canceled/refunding/refunded
    remark: str = ""  # 下单备注
    pay_time: datetime | None = None  # 支付时间
    finish_time: datetime | None = None  # 完成时间
    cancel_time: datetime | None = None  # 取消时间
    refund_time: datetime | None = None  # 退款时间
    pay_channel: str = ""  # 支付渠道：wechat/alipay/bank/cash/other
    refund_amount: Decimal | None = None  # 退款金额，支持部分退款


class RoomOrderCreate(RoomOrderBase):
    pass


class RoomOrderUpdate(BaseModel):
    order_number: str | None = None  # 生成的订单号
    ref_id: int | None = None  # 续单时为主订单主键ID，新单为 null
    user_id: int | None = None  # 下单人ID
    shop_id: int | None = None  # 门店ID
    room_id: int | None = None  # 房间ID
    order_type: str | None = None  # 订单类型：package/hourly
    source_platform: str | None = None  # 来源平台
    start_time: datetime | None = None  # 开始时间
    end_time: datetime | None = None  # 结束时间
    duration_minute: int | None = None  # 总时长，单位分钟
    order_price: Decimal | None = None  # 房间单价
    renew_price: Decimal | None = None  # 续单单价
    package_name: str | None = None  # 套餐名称
    package_price: Decimal | None = None  # 套餐总价
    package_id: int | None = None  # 套餐ID
    total_price: Decimal | None = None  # 总价
    pay_amount: Decimal | None = None  # 实际付款金额
    order_status: str | None = None  # 订单状态：created/paid/finished/canceled/refunding/refunded
    remark: str | None = None  # 下单备注
    pay_time: datetime | None = None  # 支付时间
    finish_time: datetime | None = None  # 完成时间
    cancel_time: datetime | None = None  # 取消时间
    refund_time: datetime | None = None  # 退款时间
    pay_channel: str | None = None  # 支付渠道：wechat/alipay/bank/cash/other
    refund_amount: Decimal | None = None  # 退款金额，支持部分退款


class RoomOrderOut(RoomOrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int  # 主键，自增
    tenant_id: int  # 租户ID
    is_deleted: bool  # 是否删除
    created_at: datetime  # 创建时间，插入时自动赋值
    updated_at: datetime  # 更新时间，更新时自动赋值
    deleted_at: Optional[datetime] = None  # 删除时间（软删时记录）
