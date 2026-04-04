from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.crud import user_auth as user_auth_crud
from app.schemas.common import Envelope, Paginated
from app.schemas.user_auth import UserAuthCreate, UserAuthOut, UserAuthUpdate
from app.utils.response import envelope, request_id_from_request

router = APIRouter(tags=["admin"])


@router.get("/user-auths", response_model=Envelope[Paginated[UserAuthOut]])
async def admin_list_user_auths(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await user_auth_crud.list_user_auths(session, skip=skip, limit=limit)
    data = Paginated[UserAuthOut](
        items=[UserAuthOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/user-auths/{auth_id}")
async def admin_get_user_auth(
    auth_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_auth_crud.get_user_auth(session, auth_id)
    if not row:
        raise HTTPException(404, "user auth not found")
    return envelope(data=UserAuthOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.post("/user-auths")
async def admin_create_user_auth(
    body: UserAuthCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_auth_crud.create_user_auth(session, body)
    return envelope(data=UserAuthOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.patch("/user-auths/{auth_id}")
async def admin_update_user_auth(
    auth_id: int,
    body: UserAuthUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_auth_crud.get_user_auth(session, auth_id)
    if not row:
        raise HTTPException(404, "user auth not found")
    row = await user_auth_crud.update_user_auth(session, row, body)
    return envelope(data=UserAuthOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.delete("/user-auths/{auth_id}")
async def admin_delete_user_auth(
    auth_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_auth_crud.get_user_auth(session, auth_id)
    if not row:
        raise HTTPException(404, "user auth not found")
    await user_auth_crud.soft_delete_user_auth(session, row)
    return envelope(data={"id": auth_id}, request_id=request_id_from_request(request))
