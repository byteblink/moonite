from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._util import apply_updates, soft_delete_mark
from app.models import Shop
from app.schemas.shop import ShopCreate, ShopUpdate


async def list_shops(
    session: AsyncSession, *, skip: int, limit: int
) -> tuple[list[Shop], int]:
    base = select(Shop)
    count_q = select(func.count()).select_from(Shop)
    total = int((await session.execute(count_q)).scalar_one())
    rows = (await session.execute(base.order_by(Shop.id.desc()).offset(skip).limit(limit))).scalars().all()
    return list(rows), total


async def get_shop(session: AsyncSession, shop_id: int) -> Shop | None:
    q = select(Shop).where(Shop.id == shop_id)
    return (await session.execute(q)).scalar_one_or_none()


async def create_shop(session: AsyncSession, body: ShopCreate) -> Shop:
    s = Shop(**body.model_dump())
    session.add(s)
    await session.flush()
    await session.refresh(s)
    return s


async def update_shop(session: AsyncSession, shop: Shop, body: ShopUpdate) -> Shop:
    apply_updates(shop, body.model_dump(exclude_unset=True))
    await session.flush()
    await session.refresh(shop)
    return shop


async def soft_delete_shop(session: AsyncSession, shop: Shop) -> None:
    soft_delete_mark(shop)
    await session.flush()
