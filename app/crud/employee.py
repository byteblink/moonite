from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._util import apply_updates, soft_delete_mark
from app.models import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


async def list_employees(
    session: AsyncSession, *, skip: int, limit: int
) -> tuple[list[Employee], int]:
    base = select(Employee)
    count_q = select(func.count()).select_from(Employee)
    base = base.where(Employee.is_deleted.is_(False))
    count_q = count_q.where(Employee.is_deleted.is_(False))
    total = int((await session.execute(count_q)).scalar_one())
    rows = (await session.execute(base.order_by(Employee.id.desc()).offset(skip).limit(limit))).scalars().all()
    return list(rows), total


async def get_employee(session: AsyncSession, employee_id: int) -> Employee | None:
    q = select(Employee).where(Employee.id == employee_id)
    q = q.where(Employee.is_deleted.is_(False))
    return (await session.execute(q)).scalar_one_or_none()


async def create_employee(session: AsyncSession, body: EmployeeCreate) -> Employee:
    v = Employee(**body.model_dump())
    session.add(v)
    await session.flush()
    await session.refresh(v)
    return v


async def update_employee(session: AsyncSession, v: Employee, body: EmployeeUpdate) -> Employee:
    apply_updates(v, body.model_dump(exclude_unset=True))
    await session.flush()
    await session.refresh(v)
    return v


async def soft_delete_employee(session: AsyncSession, v: Employee) -> None:
    soft_delete_mark(v)
    await session.flush()
