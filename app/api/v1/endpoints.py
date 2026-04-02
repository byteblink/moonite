from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import merchant as merchant_crud
from app.crud import order_discount as order_discount_crud
from app.crud import room as room_crud
from app.crud import room_order as room_order_crud
from app.crud import shop as shop_crud
from app.crud import user as user_crud
from app.crud import user_auth as user_auth_crud
from app.schemas.common import Paginated
from app.schemas.merchant import MerchantCreate, MerchantOut, MerchantUpdate
from app.schemas.order_discount import OrderDiscountCreate, OrderDiscountOut, OrderDiscountUpdate
from app.schemas.room import RoomCreate, RoomOut, RoomUpdate
from app.schemas.room_order import RoomOrderCreate, RoomOrderOut, RoomOrderUpdate
from app.schemas.shop import ShopCreate, ShopOut, ShopUpdate
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.schemas.user_auth import UserAuthCreate, UserAuthOut, UserAuthUpdate
from app.utils.response import envelope, request_id_from_request


from app.crud import tenant as tenant_crud
from app.crud import role as role_crud
from app.crud import employee as employee_crud
from app.crud import employee_role as employee_role_crud
from app.crud import user_tenant as user_tenant_crud

from app.schemas.tenant import TenantCreate, TenantOut, TenantUpdate
from app.schemas.role import RoleCreate, RoleOut, RoleUpdate
from app.schemas.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate
from app.schemas.employee_role import EmployeeRoleCreate, EmployeeRoleOut, EmployeeRoleUpdate
from app.schemas.user_tenant import UserTenantCreate, UserTenantOut, UserTenantUpdate
router = APIRouter(tags=["admin"])


@router.get("/merchants")
async def admin_list_merchants(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await merchant_crud.list_merchants(
        session, skip=skip, limit=limit
    )
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
    return envelope(
        data=MerchantOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


@router.post("/merchants")
async def admin_create_merchant(
    body: MerchantCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await merchant_crud.create_merchant(session, body)
    return envelope(
        data=MerchantOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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
    return envelope(
        data=MerchantOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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


@router.get("/users")
async def admin_list_users(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await user_crud.list_users(session, skip=skip, limit=limit)
    data = Paginated[UserOut](
        items=[UserOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/users/{user_id}")
async def admin_get_user(
    user_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_crud.get_user(session, user_id)
    if not row:
        raise HTTPException(404, "user not found")
    return envelope(data=UserOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.post("/users")
async def admin_create_user(
    body: UserCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_crud.create_user(session, body)
    return envelope(data=UserOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.patch("/users/{user_id}")
async def admin_update_user(
    user_id: int,
    body: UserUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_crud.get_user(session, user_id)
    if not row:
        raise HTTPException(404, "user not found")
    row = await user_crud.update_user(session, row, body)
    return envelope(data=UserOut.model_validate(row).model_dump(), request_id=request_id_from_request(request))


@router.delete("/users/{user_id}")
async def admin_delete_user(
    user_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_crud.get_user(session, user_id)
    if not row:
        raise HTTPException(404, "user not found")
    await user_crud.soft_delete_user(session, row)
    return envelope(data={"id": user_id}, request_id=request_id_from_request(request))


@router.get("/shops")
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


@router.get("/rooms")
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


@router.get("/room-orders")
async def admin_list_room_orders(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await room_order_crud.list_room_orders(
        session, skip=skip, limit=limit
    )
    data = Paginated[RoomOrderOut](
        items=[RoomOrderOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/room-orders/{order_id}")
async def admin_get_room_order(
    order_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await room_order_crud.get_room_order(session, order_id)
    if not row:
        raise HTTPException(404, "room order not found")
    return envelope(
        data=RoomOrderOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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
    return envelope(
        data=RoomOrderOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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
    return envelope(
        data=RoomOrderOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


@router.delete("/room-orders/{order_id}")
async def admin_delete_room_order(
    order_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await room_order_crud.get_room_order(session, order_id)
    if not row:
        raise HTTPException(404, "room order not found")
    await room_order_crud.soft_delete_room_order(session, row)
    return envelope(data={"id": order_id}, request_id=request_id_from_request(request))


@router.get("/order-discounts")
async def admin_list_order_discounts(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await order_discount_crud.list_order_discounts(
        session, skip=skip, limit=limit
    )
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
    return envelope(
        data=OrderDiscountOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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
    return envelope(
        data=OrderDiscountOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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


@router.get("/user-auths")
async def admin_list_user_auths(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await user_auth_crud.list_user_auths(
        session, skip=skip, limit=limit
    )
    data = Paginated[UserAuthOut](
        items=[UserAuthOut.model_validate(x) for x in items],
        total=total,
        skip=skip,
        limit=limit,
    )
    return envelope(data=data.model_dump(), request_id=request_id_from_request(request))


@router.get("/user-auths/{auth_id}")
async def admin_get_user_auth(
    auth_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_auth_crud.get_user_auth(session, auth_id)
    if not row:
        raise HTTPException(404, "user auth not found")
    return envelope(
        data=UserAuthOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


@router.post("/user-auths")
async def admin_create_user_auth(
    body: UserAuthCreate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_auth_crud.create_user_auth(session, body)
    return envelope(
        data=UserAuthOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


@router.patch("/user-auths/{auth_id}")
async def admin_update_user_auth(
    auth_id: int,
    body: UserAuthUpdate,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_auth_crud.get_user_auth(session, auth_id)
    if not row:
        raise HTTPException(404, "user auth not found")
    row = await user_auth_crud.update_user_auth(session, row, body)
    return envelope(
        data=UserAuthOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


@router.delete("/user-auths/{auth_id}")
async def admin_delete_user_auth(
    auth_id: int,
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    row = await user_auth_crud.get_user_auth(session, auth_id)
    if not row:
        raise HTTPException(404, "user auth not found")
    await user_auth_crud.soft_delete_user_auth(session, row)
    return envelope(data={"id": auth_id}, request_id=request_id_from_request(request))


@router.get("/tenants")
async def admin_list_tenants(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await tenant_crud.list_tenants(
        session, skip=skip, limit=limit
    )
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
    return envelope(
        data=TenantOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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
    return envelope(
        data=TenantOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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
    return envelope(
        data=TenantOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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


@router.get("/roles")
async def admin_list_roles(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await role_crud.list_roles(
        session, skip=skip, limit=limit
    )
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
    return envelope(
        data=RoleOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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
    return envelope(
        data=RoleOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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
    return envelope(
        data=RoleOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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


@router.get("/employees")
async def admin_list_employees(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await employee_crud.list_employees(
        session, skip=skip, limit=limit
    )
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
    return envelope(
        data=EmployeeOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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
    return envelope(
        data=EmployeeOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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
    return envelope(
        data=EmployeeOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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


@router.get("/employee-roles")
async def admin_list_employee_roles(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await employee_role_crud.list_employee_roles(
        session, skip=skip, limit=limit
    )
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


@router.get("/user-tenants")
async def admin_list_user_tenants(
    request: Request,
    session: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
):
    items, total = await user_tenant_crud.list_user_tenants(
        session, skip=skip, limit=limit
    )
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
    return envelope(
        data=UserTenantOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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
    return envelope(
        data=UserTenantOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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
    return envelope(
        data=UserTenantOut.model_validate(row).model_dump(),
        request_id=request_id_from_request(request),
    )


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
