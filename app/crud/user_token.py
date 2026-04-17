from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserToken
from datetime import UTC, datetime


async def list_user_tokens(
    session: AsyncSession, *, skip: int, limit: int
) -> tuple[list[UserToken], int]:
    base = select(UserToken)
    count_q = select(func.count()).select_from(UserToken)
    base = base.where(UserToken.is_deleted.is_(False))
    count_q = count_q.where(UserToken.is_deleted.is_(False))
    total = int((await session.execute(count_q)).scalar_one())
    rows = (await session.execute(base.order_by(UserToken.id.desc()).offset(skip).limit(limit))).scalars().all()
    return list(rows), total


async def get_user_token(session: AsyncSession, token_id: int) -> UserToken | None:
    q = select(UserToken).where(UserToken.id == token_id)
    q = q.where(UserToken.is_deleted.is_(False))
    return (await session.execute(q)).scalar_one_or_none()


async def revoke_user_token(session: AsyncSession, token: UserToken) -> UserToken:
    token.is_revoked = True
    token.revoked_at = datetime.now(UTC)
    await session.flush()
    await session.refresh(token)
    return token


async def unrevoke_user_token(session: AsyncSession, token: UserToken) -> UserToken:
    token.is_revoked = False
    token.revoked_at = None
    await session.flush()
    await session.refresh(token)
    return token


async def create_user_token(
    session: AsyncSession,
    *,
    user_id: int,
    login_type: str,
    jti: str,
    refresh_token_hash: str,
    expires_at: datetime,
    platform: str,
    user_agent: str,
    ip: str,
) -> UserToken:
    row = UserToken(
        user_id=user_id,
        login_type=login_type,
        jti=jti,
        refresh_token_hash=refresh_token_hash,
        expires_at=expires_at,
        platform=platform,
        user_agent=user_agent,
        ip=ip,
    )
    session.add(row)
    await session.flush()
    await session.refresh(row)
    return row


async def get_active_user_token_by_jti(session: AsyncSession, jti: str) -> UserToken | None:
    q = select(UserToken).where(UserToken.jti == jti)
    q = q.where(UserToken.is_deleted.is_(False), UserToken.is_revoked.is_(False))
    return (await session.execute(q)).scalar_one_or_none()


async def revoke_active_tokens_by_user(session: AsyncSession, user_id: int) -> None:
    q = select(UserToken).where(UserToken.user_id == user_id)
    q = q.where(UserToken.is_deleted.is_(False), UserToken.is_revoked.is_(False))
    rows = (await session.execute(q)).scalars().all()
    now = datetime.now(UTC)
    for row in rows:
        row.is_revoked = True
        row.revoked_at = now
    await session.flush()
