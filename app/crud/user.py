from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._util import apply_updates, soft_delete_mark
from app.models import User
from app.schemas.user import UserCreate, UserUpdate


async def list_users(
    session: AsyncSession, *, skip: int, limit: int, include_deleted: bool
) -> tuple[list[User], int]:
    base = select(User)
    count_q = select(func.count()).select_from(User)
    if not include_deleted:
        base = base.where(User.is_deleted.is_(False))
        count_q = count_q.where(User.is_deleted.is_(False))
    total = int((await session.execute(count_q)).scalar_one())
    rows = (await session.execute(base.order_by(User.id.desc()).offset(skip).limit(limit))).scalars().all()
    return list(rows), total


async def get_user(session: AsyncSession, user_id: int, *, include_deleted: bool) -> User | None:
    q = select(User).where(User.id == user_id)
    if not include_deleted:
        q = q.where(User.is_deleted.is_(False))
    return (await session.execute(q)).scalar_one_or_none()


async def create_user(session: AsyncSession, body: UserCreate) -> User:
    u = User(**body.model_dump())
    session.add(u)
    await session.flush()
    await session.refresh(u)
    return u


async def update_user(session: AsyncSession, user: User, body: UserUpdate) -> User:
    apply_updates(user, body.model_dump(exclude_unset=True))
    await session.flush()
    await session.refresh(user)
    return user


async def soft_delete_user(session: AsyncSession, user: User) -> None:
    soft_delete_mark(user)
    await session.flush()
