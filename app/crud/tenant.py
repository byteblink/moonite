from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._util import apply_updates, soft_delete_mark
from app.models import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate


async def list_tenants(
    session: AsyncSession, *, skip: int, limit: int
) -> tuple[list[Tenant], int]:
    base = select(Tenant)
    count_q = select(func.count()).select_from(Tenant)
    base = base.where(Tenant.is_deleted.is_(False))
    count_q = count_q.where(Tenant.is_deleted.is_(False))
    total = int((await session.execute(count_q)).scalar_one())
    rows = (await session.execute(base.order_by(Tenant.id.desc()).offset(skip).limit(limit))).scalars().all()
    return list(rows), total


async def get_tenant(session: AsyncSession, tenant_id: int) -> Tenant | None:
    q = select(Tenant).where(Tenant.id == tenant_id)
    q = q.where(Tenant.is_deleted.is_(False))
    return (await session.execute(q)).scalar_one_or_none()


async def create_tenant(session: AsyncSession, body: TenantCreate) -> Tenant:
    v = Tenant(**body.model_dump())
    session.add(v)
    await session.flush()
    await session.refresh(v)
    return v


async def update_tenant(session: AsyncSession, v: Tenant, body: TenantUpdate) -> Tenant:
    apply_updates(v, body.model_dump(exclude_unset=True))
    await session.flush()
    await session.refresh(v)
    return v


async def soft_delete_tenant(session: AsyncSession, v: Tenant) -> None:
    soft_delete_mark(v)
    await session.flush()
