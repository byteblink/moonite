from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._util import apply_updates, soft_delete_mark
from app.models import RoomOrder
from app.schemas.room_order import RoomOrderCreate, RoomOrderUpdate


async def list_room_orders(
    session: AsyncSession, *, skip: int, limit: int
) -> tuple[list[RoomOrder], int]:
    base = select(RoomOrder)
    count_q = select(func.count()).select_from(RoomOrder)
    base = base.where(RoomOrder.is_deleted.is_(False))
    count_q = count_q.where(RoomOrder.is_deleted.is_(False))
    total = int((await session.execute(count_q)).scalar_one())
    rows = (
        await session.execute(base.order_by(RoomOrder.id.desc()).offset(skip).limit(limit))
    ).scalars().all()
    return list(rows), total


async def get_room_order(session: AsyncSession, order_id: int) -> RoomOrder | None:
    q = select(RoomOrder).where(RoomOrder.id == order_id)
    q = q.where(RoomOrder.is_deleted.is_(False))
    return (await session.execute(q)).scalar_one_or_none()


async def create_room_order(session: AsyncSession, body: RoomOrderCreate) -> RoomOrder:
    o = RoomOrder(**body.model_dump())
    session.add(o)
    await session.flush()
    await session.refresh(o)
    return o


async def update_room_order(session: AsyncSession, order: RoomOrder, body: RoomOrderUpdate) -> RoomOrder:
    apply_updates(order, body.model_dump(exclude_unset=True))
    await session.flush()
    await session.refresh(order)
    return order


async def soft_delete_room_order(session: AsyncSession, order: RoomOrder) -> None:
    soft_delete_mark(order)
    await session.flush()
