from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.crud import room_order as room_order_crud
from app.schemas.common import Envelope, Paginated
from app.schemas.room_order import RoomOrderCreate, RoomOrderOut, RoomOrderUpdate
from app.utils.response import envelope, request_id_from_request

router = APIRouter(tags=["admin"])


@router.get("/room-orders", response_model=Envelope[Paginated[RoomOrderOut]])
async def admin_list_room_orders(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await room_order_crud.list_room_orders(session, skip=skip, limit=limit)
    data = Paginated[RoomOrderOut](
        items=[RoomOrderOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/room-orders/{order_id}")
async def admin_get_room_order(order_id: int, request: Request, session: AsyncSession = Depends(get_db)):
    row = await room_order_crud.get_room_order(session, order_id)
    if not row:
        raise HTTPException(404, "room order not found")
    return envelope(data=RoomOrderOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.post("/room-orders")
async def admin_create_room_order(
    body: RoomOrderCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    try:
        row = await room_order_crud.create_room_order(session, body)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, "order_number conflict or foreign key violation") from None
    return envelope(data=RoomOrderOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.patch("/room-orders/{order_id}")
async def admin_update_room_order(
    order_id: int,
    body: RoomOrderUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await room_order_crud.get_room_order(session, order_id)
    if not row:
        raise HTTPException(404, "room order not found")
    try:
        row = await room_order_crud.update_room_order(session, row, body)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, "order_number conflict or foreign key violation") from None
    return envelope(data=RoomOrderOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.delete("/room-orders/{order_id}")
async def admin_delete_room_order(order_id: int, request: Request, session: AsyncSession = Depends(get_db)):
    row = await room_order_crud.get_room_order(session, order_id)
    if not row:
        raise HTTPException(404, "room order not found")
    await room_order_crud.soft_delete_room_order(session, row)
    return envelope(data={"id": order_id}, request_id=request_id_from_request(request))
