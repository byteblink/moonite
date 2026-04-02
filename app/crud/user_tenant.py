from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._util import apply_updates, soft_delete_mark
from app.models import UserTenant
from app.schemas.user_tenant import UserTenantCreate, UserTenantUpdate


async def list_user_tenants(
    session: AsyncSession, *, skip: int, limit: int
) -> tuple[list[UserTenant], int]:
    base = select(UserTenant)
    count_q = select(func.count()).select_from(UserTenant)
    base = base.where(UserTenant.is_deleted.is_(False))
    count_q = count_q.where(UserTenant.is_deleted.is_(False))
    total = int((await session.execute(count_q)).scalar_one())
    rows = (await session.execute(base.order_by(UserTenant.id.desc()).offset(skip).limit(limit))).scalars().all()
    return list(rows), total


async def get_user_tenant(session: AsyncSession, user_tenant_id: int) -> UserTenant | None:
    q = select(UserTenant).where(UserTenant.id == user_tenant_id)
    q = q.where(UserTenant.is_deleted.is_(False))
    return (await session.execute(q)).scalar_one_or_none()


async def create_user_tenant(session: AsyncSession, body: UserTenantCreate) -> UserTenant:
    v = UserTenant(**body.model_dump())
    session.add(v)
    await session.flush()
    await session.refresh(v)
    return v


async def update_user_tenant(session: AsyncSession, v: UserTenant, body: UserTenantUpdate) -> UserTenant:
    apply_updates(v, body.model_dump(exclude_unset=True))
    await session.flush()
    await session.refresh(v)
    return v


async def soft_delete_user_tenant(session: AsyncSession, v: UserTenant) -> None:
    soft_delete_mark(v)
    await session.flush()
