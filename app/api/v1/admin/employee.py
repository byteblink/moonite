from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import employee as employee_crud
from app.schemas.common import Envelope, Paginated
from app.schemas.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate
from app.utils.response import envelope, request_id_from_request

router = APIRouter(tags=["admin"])


@router.get("/employees", response_model=Envelope[Paginated[EmployeeOut]])
async def admin_list_employees(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await employee_crud.list_employees(session, skip=skip, limit=limit)
    data = Paginated[EmployeeOut](
        items=[EmployeeOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/employees/{employee_id}")
async def admin_get_employee(
    employee_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await employee_crud.get_employee(session, employee_id)
    if not row:
        raise HTTPException(404, "employee not found")
    return envelope(data=EmployeeOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.post("/employees")
async def admin_create_employee(
    body: EmployeeCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    try:
        row = await employee_crud.create_employee(session, body)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, "conflict or foreign key violation") from None
    return envelope(data=EmployeeOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.patch("/employees/{employee_id}")
async def admin_update_employee(
    employee_id: int,
    body: EmployeeUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await employee_crud.get_employee(session, employee_id)
    if not row:
        raise HTTPException(404, "employee not found")
    try:
        row = await employee_crud.update_employee(session, row, body)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, "conflict or foreign key violation") from None
    return envelope(data=EmployeeOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.delete("/employees/{employee_id}")
async def admin_delete_employee(
    employee_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await employee_crud.get_employee(session, employee_id)
    if not row:
        raise HTTPException(404, "employee not found")
    await employee_crud.soft_delete_employee(session, row)
    return envelope(data={"id": employee_id}, request_id=request_id_from_request(request))
