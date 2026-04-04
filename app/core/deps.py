from collections.abc import AsyncGenerator
from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.context import CurrentContext
from app.core.database import AsyncSessionLocal


async def get_current_context(request: Request) -> CurrentContext:
    user_id = getattr(request.state, "user_id", None)
    tenant_id = getattr(request.state, "tenant_id", None)

    if not user_id or not tenant_id:
        raise HTTPException(status_code=401, detail="unauthorized")

    return CurrentContext(user_id=user_id, tenant_id=tenant_id)


async def get_db(
    current: CurrentContext = Depends(get_current_context),
) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        session.info["tenant_id"] = current.tenant_id
        session.info["user_id"] = current.user_id
        yield session