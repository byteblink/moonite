from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._util import apply_updates, soft_delete_mark
from app.models import EmployeeRole
from app.schemas.employee_role import EmployeeRoleCreate, EmployeeRoleUpdate


async def list_employee_roles(
    session: AsyncSession, *, skip: int, limit: int
) -> tuple[list[EmployeeRole], int]:
    base = select(EmployeeRole)
    count_q = select(func.count()).select_from(EmployeeRole)
    base = base.where(EmployeeRole.is_deleted.is_(False))
    count_q = count_q.where(EmployeeRole.is_deleted.is_(False))
    total = int((await session.execute(count_q)).scalar_one())
    rows = (await session.execute(base.order_by(EmployeeRole.id.desc()).offset(skip).limit(limit))).scalars().all()
    return list(rows), total


async def get_employee_role(session: AsyncSession, employee_role_id: int) -> EmployeeRole | None:
    q = select(EmployeeRole).where(EmployeeRole.id == employee_role_id)
    q = q.where(EmployeeRole.is_deleted.is_(False))
    return (await session.execute(q)).scalar_one_or_none()


async def create_employee_role(session: AsyncSession, body: EmployeeRoleCreate) -> EmployeeRole:
    v = EmployeeRole(**body.model_dump())
    session.add(v)
    await session.flush()
    await session.refresh(v)
    return v


async def update_employee_role(session: AsyncSession, v: EmployeeRole, body: EmployeeRoleUpdate) -> EmployeeRole:
    apply_updates(v, body.model_dump(exclude_unset=True))
    await session.flush()
    await session.refresh(v)
    return v


async def soft_delete_employee_role(session: AsyncSession, v: EmployeeRole) -> None:
    soft_delete_mark(v)
    await session.flush()
