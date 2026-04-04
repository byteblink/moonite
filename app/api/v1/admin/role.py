from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.crud import role as role_crud
from app.schemas.common import Envelope, Paginated
from app.schemas.role import RoleCreate, RoleOut, RoleUpdate
from app.utils.response import envelope, request_id_from_request

router = APIRouter(tags=["admin"])


@router.get("/roles", response_model=Envelope[Paginated[RoleOut]])
async def admin_list_roles(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await role_crud.list_roles(session, skip=skip, limit=limit)
    data = Paginated[RoleOut](
        items=[RoleOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/roles/{role_id}")
async def admin_get_role(
    role_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await role_crud.get_role(session, role_id)
    if not row:
        raise HTTPException(404, "role not found")
    return envelope(data=RoleOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.post("/roles")
async def admin_create_role(
    body: RoleCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    try:
        row = await role_crud.create_role(session, body)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, "conflict or foreign key violation") from None
    return envelope(data=RoleOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.patch("/roles/{role_id}")
async def admin_update_role(
    role_id: int,
    body: RoleUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await role_crud.get_role(session, role_id)
    if not row:
        raise HTTPException(404, "role not found")
    try:
        row = await role_crud.update_role(session, row, body)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, "conflict or foreign key violation") from None
    return envelope(data=RoleOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.delete("/roles/{role_id}")
async def admin_delete_role(
    role_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await role_crud.get_role(session, role_id)
    if not row:
        raise HTTPException(404, "role not found")
    await role_crud.soft_delete_role(session, row)
    return envelope(data={"id": role_id}, request_id=request_id_from_request(request))
