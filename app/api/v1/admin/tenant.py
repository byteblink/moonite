from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.crud import tenant as tenant_crud
from app.schemas.common import Envelope, Paginated
from app.schemas.tenant import TenantCreate, TenantOut, TenantUpdate
from app.utils.response import envelope, request_id_from_request

router = APIRouter(tags=["admin"])


@router.get("/tenants", response_model=Envelope[Paginated[TenantOut]])
async def admin_list_tenants(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await tenant_crud.list_tenants(session, skip=skip, limit=limit)
    data = Paginated[TenantOut](
        items=[TenantOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/tenants/{tenant_id}")
async def admin_get_tenant(
    tenant_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await tenant_crud.get_tenant(session, tenant_id)
    if not row:
        raise HTTPException(404, "tenant not found")
    return envelope(data=TenantOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.post("/tenants")
async def admin_create_tenant(
    body: TenantCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    try:
        row = await tenant_crud.create_tenant(session, body)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, "conflict or foreign key violation") from None
    return envelope(data=TenantOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.patch("/tenants/{tenant_id}")
async def admin_update_tenant(
    tenant_id: int,
    body: TenantUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await tenant_crud.get_tenant(session, tenant_id)
    if not row:
        raise HTTPException(404, "tenant not found")
    try:
        row = await tenant_crud.update_tenant(session, row, body)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, "conflict or foreign key violation") from None
    return envelope(data=TenantOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.delete("/tenants/{tenant_id}")
async def admin_delete_tenant(
    tenant_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await tenant_crud.get_tenant(session, tenant_id)
    if not row:
        raise HTTPException(404, "tenant not found")
    await tenant_crud.soft_delete_tenant(session, row)
    return envelope(data={"id": tenant_id}, request_id=request_id_from_request(request))
