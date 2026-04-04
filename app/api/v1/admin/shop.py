from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.crud import shop as shop_crud
from app.schemas.common import Envelope, Paginated
from app.schemas.shop import ShopCreate, ShopOut, ShopUpdate
from app.utils.response import envelope, request_id_from_request

router = APIRouter(tags=["admin"])


@router.get("/shops", response_model=Envelope[Paginated[ShopOut]])
async def admin_list_shops(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await shop_crud.list_shops(session, skip=skip, limit=limit)
    data = Paginated[ShopOut](
        items=[ShopOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/shops/{shop_id}")
async def admin_get_shop(
    shop_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await shop_crud.get_shop(session, shop_id)
    if not row:
        raise HTTPException(404, "shop not found")
    return envelope(data=ShopOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.post("/shops")
async def admin_create_shop(
    body: ShopCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await shop_crud.create_shop(session, body)
    return envelope(data=ShopOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.patch("/shops/{shop_id}")
async def admin_update_shop(
    shop_id: int,
    body: ShopUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await shop_crud.get_shop(session, shop_id)
    if not row:
        raise HTTPException(404, "shop not found")
    row = await shop_crud.update_shop(session, row, body)
    return envelope(data=ShopOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.delete("/shops/{shop_id}")
async def admin_delete_shop(
    shop_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await shop_crud.get_shop(session, shop_id)
    if not row:
        raise HTTPException(404, "shop not found")
    await shop_crud.soft_delete_shop(session, row)
    return envelope(data={"id": shop_id}, request_id=request_id_from_request(request))
