from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud._util import apply_updates, soft_delete_mark
from app.models import UserAuth
from app.schemas.user_auth import UserAuthCreate, UserAuthUpdate


async def list_user_auths(
    session: AsyncSession, *, skip: int, limit: int
) -> tuple[list[UserAuth], int]:
    base = select(UserAuth)
    count_q = select(func.count()).select_from(UserAuth)
    base = base.where(UserAuth.is_deleted.is_(False))
    count_q = count_q.where(UserAuth.is_deleted.is_(False))
    total = int((await session.execute(count_q)).scalar_one())
    rows = (
        await session.execute(base.order_by(UserAuth.id.desc()).offset(skip).limit(limit))
    ).scalars().all()
    return list(rows), total


async def get_user_auth(session: AsyncSession, auth_id: int) -> UserAuth | None:
    q = select(UserAuth).where(UserAuth.id == auth_id)
    q = q.where(UserAuth.is_deleted.is_(False))
    return (await session.execute(q)).scalar_one_or_none()


async def create_user_auth(session: AsyncSession, body: UserAuthCreate) -> UserAuth:
    a = UserAuth(**body.model_dump())
    session.add(a)
    await session.flush()
    await session.refresh(a)
    return a


async def update_user_auth(session: AsyncSession, auth: UserAuth, body: UserAuthUpdate) -> UserAuth:
    apply_updates(auth, body.model_dump(exclude_unset=True))
    await session.flush()
    await session.refresh(auth)
    return auth


async def soft_delete_user_auth(session: AsyncSession, auth: UserAuth) -> None:
    soft_delete_mark(auth)
    await session.flush()
