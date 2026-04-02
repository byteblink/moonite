from fastapi import APIRouter

from app.api.v1.admin.employee import router as employee_router
from app.api.v1.admin.employee_role import router as employee_role_router
from app.api.v1.admin.merchant import router as merchant_router
from app.api.v1.admin.order_discount import router as order_discount_router
from app.api.v1.admin.role import router as role_router
from app.api.v1.admin.room import router as room_router
from app.api.v1.admin.room_order import router as room_order_router
from app.api.v1.admin.shop import router as shop_router
from app.api.v1.admin.tenant import router as tenant_router
from app.api.v1.admin.user import router as user_router
from app.api.v1.admin.user_auth import router as user_auth_router
from app.api.v1.admin.user_tenant import router as user_tenant_router

router = APIRouter(tags=["admin"])

router.include_router(merchant_router)
router.include_router(user_router)
router.include_router(shop_router)
router.include_router(room_router)
router.include_router(room_order_router)
router.include_router(order_discount_router)
router.include_router(user_auth_router)
router.include_router(tenant_router)
router.include_router(role_router)
router.include_router(employee_router)
router.include_router(employee_role_router)
router.include_router(user_tenant_router)
