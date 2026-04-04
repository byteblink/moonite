from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._util import apply_updates, soft_delete_mark
from app.models import Merchant
from app.schemas.merchant import MerchantCreate, MerchantUpdate


async def list_merchants(
    session: AsyncSession, *, skip: int, limit: int
) -> tuple[list[Merchant], int]:
    base = select(Merchant)
    count_q = select(func.count()).select_from(Merchant)
    total = int((await session.execute(count_q)).scalar_one())
    rows = (
        await session.execute(base.order_by(Merchant.id.desc()).offset(skip).limit(limit))
    ).scalars().all()
    return list(rows), total


async def get_merchant(session: AsyncSession, merchant_id: int) -> Merchant | None:
    q = select(Merchant).where(Merchant.id == merchant_id)
    return (await session.execute(q)).scalar_one_or_none()


async def create_merchant(session: AsyncSession, body: MerchantCreate) -> Merchant:
    m = Merchant(**body.model_dump())
    session.add(m)
    await session.flush()
    await session.refresh(m)
    return m


async def update_merchant(session: AsyncSession, merchant: Merchant, body: MerchantUpdate) -> Merchant:
    apply_updates(merchant, body.model_dump(exclude_unset=True))
    await session.flush()
    await session.refresh(merchant)
    return merchant


async def soft_delete_merchant(session: AsyncSession, merchant: Merchant) -> None:
    soft_delete_mark(merchant)
    await session.flush()
