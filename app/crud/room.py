from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._util import apply_updates, soft_delete_mark
from app.models import Room
from app.schemas.room import RoomCreate, RoomUpdate


async def list_rooms(
    session: AsyncSession, *, skip: int, limit: int
) -> tuple[list[Room], int]:
    base = select(Room)
    count_q = select(func.count()).select_from(Room)
    base = base.where(Room.is_deleted.is_(False))
    count_q = count_q.where(Room.is_deleted.is_(False))
    total = int((await session.execute(count_q)).scalar_one())
    rows = (await session.execute(base.order_by(Room.id.desc()).offset(skip).limit(limit))).scalars().all()
    return list(rows), total


async def get_room(session: AsyncSession, room_id: int) -> Room | None:
    q = select(Room).where(Room.id == room_id)
    q = q.where(Room.is_deleted.is_(False))
    return (await session.execute(q)).scalar_one_or_none()


async def create_room(session: AsyncSession, body: RoomCreate) -> Room:
    r = Room(**body.model_dump())
    session.add(r)
    await session.flush()
    await session.refresh(r)
    return r


async def update_room(session: AsyncSession, room: Room, body: RoomUpdate) -> Room:
    apply_updates(room, body.model_dump(exclude_unset=True))
    await session.flush()
    await session.refresh(room)
    return room


async def soft_delete_room(session: AsyncSession, room: Room) -> None:
    soft_delete_mark(room)
    await session.flush()
