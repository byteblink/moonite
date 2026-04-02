from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import employee_role as employee_role_crud
from app.schemas.common import Envelope, Paginated
from app.schemas.employee_role import EmployeeRoleCreate, EmployeeRoleOut, EmployeeRoleUpdate
from app.utils.response import envelope, request_id_from_request

router = APIRouter(tags=["admin"])


@router.get("/employee-roles", response_model=Envelope[Paginated[EmployeeRoleOut]])
async def admin_list_employee_roles(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await employee_role_crud.list_employee_roles(session, skip=skip, limit=limit)
    data = Paginated[EmployeeRoleOut](
        items=[EmployeeRoleOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/employee-roles/{employee_role_id}")
async def admin_get_employee_role(
    employee_role_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await employee_role_crud.get_employee_role(session, employee_role_id)
    if not row:
        raise HTTPException(404, "employee_role not found")
    return envelope(
        data=EmployeeRoleOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


@router.post("/employee-roles")
async def admin_create_employee_role(
    body: EmployeeRoleCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    try:
        row = await employee_role_crud.create_employee_role(session, body)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, "conflict or foreign key violation") from None
    return envelope(
        data=EmployeeRoleOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


@router.patch("/employee-roles/{employee_role_id}")
async def admin_update_employee_role(
    employee_role_id: int,
    body: EmployeeRoleUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await employee_role_crud.get_employee_role(session, employee_role_id)
    if not row:
        raise HTTPException(404, "employee_role not found")
    try:
        row = await employee_role_crud.update_employee_role(session, row, body)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, "conflict or foreign key violation") from None
    return envelope(
        data=EmployeeRoleOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


@router.delete("/employee-roles/{employee_role_id}")
async def admin_delete_employee_role(
    employee_role_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await employee_role_crud.get_employee_role(session, employee_role_id)
    if not row:
        raise HTTPException(404, "employee_role not found")
    await employee_role_crud.soft_delete_employee_role(session, row)
    return envelope(data={"id": employee_role_id}, request_id=request_id_from_request(request))
