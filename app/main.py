from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1 import endpoints
from app.api.v1.routes import api_router
from app.core.config import settings
from app.core.database import engine
from app.core.logger import logger
from app.utils.response import envelope, request_id_from_request


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting {}", settings.app_name)
    yield
    await engine.dispose()
    logger.info("shutdown complete")


app = FastAPI(title=settings.app_name, lifespan=lifespan)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=envelope(
            code=exc.status_code,
            message=str(exc.detail),
            data=None,
            request_id=request_id_from_request(request),
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
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


app.include_router(endpoints.router, prefix="/admin")
app.include_router(api_router, prefix="/api/v1")
