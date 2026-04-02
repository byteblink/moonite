from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import user_token as user_token_crud
from app.schemas.common import Envelope, Paginated
from app.schemas.user_token import UserTokenOut
from app.utils.response import envelope, request_id_from_request

router = APIRouter(tags=["admin"])


@router.get("/user-tokens", response_model=Envelope[Paginated[UserTokenOut]])
async def admin_list_user_tokens(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await user_token_crud.list_user_tokens(session, skip=skip, limit=limit)
    data = Paginated[UserTokenOut](
        items=[UserTokenOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.patch("/user-tokens/{token_id}/revoke")
async def admin_revoke_user_token(
    token_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_token_crud.get_user_token(session, token_id)
    if not row:
        raise HTTPException(404, "user token not found")
    row = await user_token_crud.revoke_user_token(session, row)
    return envelope(data=UserTokenOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))
