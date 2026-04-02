from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._util import apply_updates, soft_delete_mark
from app.models import OrderDiscount
from app.schemas.order_discount import OrderDiscountCreate, OrderDiscountUpdate


async def list_order_discounts(
    session: AsyncSession, *, skip: int, limit: int
) -> tuple[list[OrderDiscount], int]:
    base = select(OrderDiscount)
    count_q = select(func.count()).select_from(OrderDiscount)
    base = base.where(OrderDiscount.is_deleted.is_(False))
    count_q = count_q.where(OrderDiscount.is_deleted.is_(False))
    total = int((await session.execute(count_q)).scalar_one())
    rows = (
        await session.execute(base.order_by(OrderDiscount.id.desc()).offset(skip).limit(limit))
    ).scalars().all()
    return list(rows), total


async def get_order_discount(
    session: AsyncSession, discount_id: int) -> OrderDiscount | None:
    q = select(OrderDiscount).where(OrderDiscount.id == discount_id)
    q = q.where(OrderDiscount.is_deleted.is_(False))
    return (await session.execute(q)).scalar_one_or_none()


async def create_order_discount(session: AsyncSession, body: OrderDiscountCreate) -> OrderDiscount:
    d = OrderDiscount(**body.model_dump())
    session.add(d)
    await session.flush()
    await session.refresh(d)
    return d


async def update_order_discount(
    session: AsyncSession, discount: OrderDiscount, body: OrderDiscountUpdate
) -> OrderDiscount:
    apply_updates(discount, body.model_dump(exclude_unset=True))
    await session.flush()
    await session.refresh(discount)
    return discount


async def soft_delete_order_discount(session: AsyncSession, discount: OrderDiscount) -> None:
    soft_delete_mark(discount)
    await session.flush()
