from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.crud import merchant as merchant_crud
from app.schemas.common import Envelope, Paginated
from app.schemas.merchant import MerchantCreate, MerchantOut, MerchantUpdate
from app.utils.response import envelope, request_id_from_request

router = APIRouter(tags=["admin"])


@router.get("/merchants", response_model=Envelope[Paginated[MerchantOut]])
async def admin_list_merchants(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await merchant_crud.list_merchants(session, skip=skip, limit=limit)
    data = Paginated[MerchantOut](
        items=[MerchantOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/merchants/{merchant_id}")
async def admin_get_merchant(
    merchant_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await merchant_crud.get_merchant(session, merchant_id)
    if not row:
        raise HTTPException(404, "merchant not found")
    return envelope(data=MerchantOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.post("/merchants")
async def admin_create_merchant(
    body: MerchantCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await merchant_crud.create_merchant(session, body)
    return envelope(data=MerchantOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.patch("/merchants/{merchant_id}")
async def admin_update_merchant(
    merchant_id: int,
    body: MerchantUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await merchant_crud.get_merchant(session, merchant_id)
    if not row:
        raise HTTPException(404, "merchant not found")
    row = await merchant_crud.update_merchant(session, row, body)
    return envelope(data=MerchantOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.delete("/merchants/{merchant_id}")
async def admin_delete_merchant(
    merchant_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await merchant_crud.get_merchant(session, merchant_id)
    if not row:
        raise HTTPException(404, "merchant not found")
    await merchant_crud.soft_delete_merchant(session, row)
    return envelope(data={"id": merchant_id}, request_id=request_id_from_request(request))
