from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.crud import user as user_crud
from app.schemas.common import Envelope, Paginated
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.utils.response import envelope, request_id_from_request

router = APIRouter(tags=["admin"])


@router.get("/users", response_model=Envelope[Paginated[UserOut]])
async def admin_list_users(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await user_crud.list_users(session, skip=skip, limit=limit)
    # 去掉 password 字段
    result_items = []
    for x in items:
        data_dict = UserOut.model_validate(x).model_dump()
        data_dict.pop("password", None)
        result_items.append(data_dict)
    data = Paginated[dict](
        items=result_items,
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/users/{user_id}")
async def admin_get_user(
    user_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_crud.get_user(session, user_id)
    if not row:
        raise HTTPException(404, "user not found")
    return envelope(data=UserOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.post("/users")
async def admin_create_user(
    body: UserCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_crud.create_user(session, body)
    return envelope(data=UserOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.patch("/users/{user_id}")
async def admin_update_user(
    user_id: int,
    body: UserUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_crud.get_user(session, user_id)
    if not row:
        raise HTTPException(404, "user not found")
    row = await user_crud.update_user(session, row, body)
    return envelope(data=UserOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.delete("/users/{user_id}")
async def admin_delete_user(
    user_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_crud.get_user(session, user_id)
    if not row:
        raise HTTPException(404, "user not found")
    await user_crud.soft_delete_user(session, row)
    return envelope(data={"id": user_id}, request_id=request_id_from_request(request))
