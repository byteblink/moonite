from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Identity, Integer, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class RoomOrder(Base):
    __tablename__ = "room_orders"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True, comment="主键，自增")
    tenant_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=False, comment="租户ID")
    order_number: Mapped[str] = mapped_column(String(50), nullable=False, comment="生成的订单号")
    ref_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("room_orders.id", ondelete="SET NULL"), nullable=True, comment="续单时为主订单主键ID，新单为 null"
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="下单人ID"
    )
    shop_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("shops.id", ondelete="SET NULL"), nullable=True, comment="门店ID"
    )
    room_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True, comment="房间ID"
    )
    order_type: Mapped[str] = mapped_column(String(8), nullable=False, server_default="", comment="订单类型：package/hourly")
    source_platform: Mapped[str] = mapped_column(String(8), nullable=False, server_default="", comment="来源平台")
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="开始时间")
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="结束时间")
    duration_minute: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0", comment="总时长，单位分钟")
    order_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="房间单价")
    renew_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="续单单价")
    package_name: Mapped[str] = mapped_column(String(50), nullable=False, server_default="", comment="套餐名称")
    package_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="套餐总价")
    package_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, comment="套餐ID")
    total_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="总价")
    pay_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="实际付款金额")
    order_status: Mapped[str] = mapped_column(String(8), nullable=False, server_default="created", comment="订单状态：created/paid/finished/canceled/refunding/refunded")
    remark: Mapped[str] = mapped_column(String(200), nullable=False, server_default="", comment="下单备注")
    pay_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="支付时间")
    finish_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="完成时间")
    cancel_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="取消时间")
    refund_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="退款时间")
    pay_channel: Mapped[str] = mapped_column(String(4), nullable=False, server_default="", comment="支付渠道：wechat/alipay/bank/cash/other")
    refund_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="退款金额，支持部分退款")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false", comment="是否删除")
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="删除时间（软删时记录）")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="创建时间，插入时自动赋值"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), comment="更新时间，更新时自动赋值"
    )
