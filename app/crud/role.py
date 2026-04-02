from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._util import apply_updates, soft_delete_mark
from app.models import Role
from app.schemas.role import RoleCreate, RoleUpdate


async def list_roles(
    session: AsyncSession, *, skip: int, limit: int
) -> tuple[list[Role], int]:
    base = select(Role)
    count_q = select(func.count()).select_from(Role)
    base = base.where(Role.is_deleted.is_(False))
    count_q = count_q.where(Role.is_deleted.is_(False))
    total = int((await session.execute(count_q)).scalar_one())
    rows = (await session.execute(base.order_by(Role.id.desc()).offset(skip).limit(limit))).scalars().all()
    return list(rows), total


async def get_role(session: AsyncSession, role_id: int) -> Role | None:
    q = select(Role).where(Role.id == role_id)
    q = q.where(Role.is_deleted.is_(False))
    return (await session.execute(q)).scalar_one_or_none()


async def create_role(session: AsyncSession, body: RoleCreate) -> Role:
    v = Role(**body.model_dump())
    session.add(v)
    await session.flush()
    await session.refresh(v)
    return v


async def update_role(session: AsyncSession, v: Role, body: RoleUpdate) -> Role:
    apply_updates(v, body.model_dump(exclude_unset=True))
    await session.flush()
    await session.refresh(v)
    return v


async def soft_delete_role(session: AsyncSession, v: Role) -> None:
    soft_delete_mark(v)
    await session.flush()
