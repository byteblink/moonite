from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.admin import router as admin_router
from app.api.v1.routes import api_router
from app.core.config import settings
from app.core.database import engine
from app.core.exceptions import BusinessException
from app.core.logger import logger
from app.utils.response import envelope, request_id_from_request


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting {}", settings.app_name)
    yield
    await engine.dispose()
    logger.info("shutdown complete")


app = FastAPI(title=settings.app_name, lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_context_middleware(request: Request, call_next):
    # Try to extract user_id and tenant_id from JWT
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        token = auth_header[7:].strip()
        try:
            from app.utils.auth import decode_jwt
            claims = decode_jwt(token)
            if claims.get("type") == "access":
                request.state.user_id = int(claims.get("sub", 0))
                request.state.tenant_id = int(claims.get("tid", 0))
        except Exception:
            pass
    
    response = await call_next(request)
    return response


@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content=envelope(
            code=exc.code,
            message=exc.message,
            data=exc.data,
            request_id=request_id_from_request(request),
        ),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    # 仅对 /admin 下的业务请求返回 200，其它维持原样 (或根据需求统一)
    status_code = exc.status_code
    if request.url.path.startswith("/admin"):
        status_code = 200

    return JSONResponse(
        status_code=status_code,
        content=envelope(
            code=exc.status_code,
            message=str(exc.detail),
            data=None,
            request_id=request_id_from_request(request),
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    status_code = 422
    if request.url.path.startswith("/admin"):
        status_code = 200

    return JSONResponse(
        status_code=status_code,
        content=envelope(
            code=422,
            message="validation error",
            data={"errors": exc.errors()},
            request_id=request_id_from_request(request),
        ),
    )


@app.get("/health")
async def health(request: Request):
    return envelope(data={"status": "ok"}, request_id=request_id_from_request(request))


app.include_router(admin_router, prefix="/admin")
app.include_router(api_router, prefix="/web")
