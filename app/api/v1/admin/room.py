from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.crud import room as room_crud
from app.schemas.common import Envelope, Paginated
from app.schemas.room import RoomCreate, RoomOut, RoomUpdate
from app.utils.response import envelope, request_id_from_request

router = APIRouter(tags=["admin"])


@router.get("/rooms", response_model=Envelope[Paginated[RoomOut]])
async def admin_list_rooms(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await room_crud.list_rooms(session, skip=skip, limit=limit)
    data = Paginated[RoomOut](
        items=[RoomOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/rooms/{room_id}")
async def admin_get_room(
    room_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await room_crud.get_room(session, room_id)
    if not row:
        raise HTTPException(404, "room not found")
    return envelope(data=RoomOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.post("/rooms")
async def admin_create_room(
    body: RoomCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await room_crud.create_room(session, body)
    return envelope(data=RoomOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.patch("/rooms/{room_id}")
async def admin_update_room(
    room_id: int,
    body: RoomUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await room_crud.get_room(session, room_id)
    if not row:
        raise HTTPException(404, "room not found")
    row = await room_crud.update_room(session, row, body)
    return envelope(data=RoomOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.delete("/rooms/{room_id}")
async def admin_delete_room(
    room_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await room_crud.get_room(session, room_id)
    if not row:
        raise HTTPException(404, "room not found")
    await room_crud.soft_delete_room(session, row)
    return envelope(data={"id": room_id}, request_id=request_id_from_request(request))
