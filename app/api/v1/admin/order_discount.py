from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.crud import order_discount as order_discount_crud
from app.schemas.common import Envelope, Paginated
from app.schemas.order_discount import OrderDiscountCreate, OrderDiscountOut, OrderDiscountUpdate
from app.utils.response import envelope, request_id_from_request

router = APIRouter(tags=["admin"])


@router.get("/order-discounts", response_model=Envelope[Paginated[OrderDiscountOut]])
async def admin_list_order_discounts(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await order_discount_crud.list_order_discounts(session, skip=skip, limit=limit)
    data = Paginated[OrderDiscountOut](
        items=[OrderDiscountOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/order-discounts/{discount_id}")
async def admin_get_order_discount(
    discount_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await order_discount_crud.get_order_discount(session, discount_id)
    if not row:
        raise HTTPException(404, "order discount not found")
    return envelope(
        data=OrderDiscountOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


@router.post("/order-discounts")
async def admin_create_order_discount(
    body: OrderDiscountCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await order_discount_crud.create_order_discount(session, body)
    return envelope(data=OrderDiscountOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.patch("/order-discounts/{discount_id}")
async def admin_update_order_discount(
    discount_id: int,
    body: OrderDiscountUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await order_discount_crud.get_order_discount(session, discount_id)
    if not row:
        raise HTTPException(404, "order discount not found")
    row = await order_discount_crud.update_order_discount(session, row, body)
    return envelope(data=OrderDiscountOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.delete("/order-discounts/{discount_id}")
async def admin_delete_order_discount(
    discount_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await order_discount_crud.get_order_discount(session, discount_id)
    if not row:
        raise HTTPException(404, "order discount not found")
    await order_discount_crud.soft_delete_order_discount(session, row)
    return envelope(data={"id": discount_id}, request_id=request_id_from_request(request))
