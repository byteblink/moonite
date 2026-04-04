from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.crud import user_tenant as user_tenant_crud
from app.schemas.common import Envelope, Paginated
from app.schemas.user_tenant import UserTenantCreate, UserTenantOut, UserTenantUpdate
from app.utils.response import envelope, request_id_from_request

router = APIRouter(tags=["admin"])


@router.get("/user-tenants", response_model=Envelope[Paginated[UserTenantOut]])
async def admin_list_user_tenants(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await user_tenant_crud.list_user_tenants(session, skip=skip, limit=limit)
    data = Paginated[UserTenantOut](
        items=[UserTenantOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/user-tenants/{user_tenant_id}")
async def admin_get_user_tenant(
    user_tenant_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_tenant_crud.get_user_tenant(session, user_tenant_id)
    if not row:
        raise HTTPException(404, "user_tenant not found")
    return envelope(data=UserTenantOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.post("/user-tenants")
async def admin_create_user_tenant(
    body: UserTenantCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    try:
        row = await user_tenant_crud.create_user_tenant(session, body)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, "conflict or foreign key violation") from None
    return envelope(data=UserTenantOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.patch("/user-tenants/{user_tenant_id}")
async def admin_update_user_tenant(
    user_tenant_id: int,
    body: UserTenantUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_tenant_crud.get_user_tenant(session, user_tenant_id)
    if not row:
        raise HTTPException(404, "user_tenant not found")
    try:
        row = await user_tenant_crud.update_user_tenant(session, row, body)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, "conflict or foreign key violation") from None
    return envelope(data=UserTenantOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.delete("/user-tenants/{user_tenant_id}")
async def admin_delete_user_tenant(
    user_tenant_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_tenant_crud.get_user_tenant(session, user_tenant_id)
    if not row:
        raise HTTPException(404, "user_tenant not found")
    await user_tenant_crud.soft_delete_user_tenant(session, row)
    return envelope(data={"id": user_tenant_id}, request_id=request_id_from_request(request))
