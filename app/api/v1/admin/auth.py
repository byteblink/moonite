from datetime import UTC, datetime

import jwt
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_session
from app.crud import user as user_crud
from app.crud import user_token as user_token_crud
from app.schemas.common import Envelope
from app.schemas.user import UserCreate
from app.schemas.user import UserOut
from app.utils.auth import create_jwt, decode_jwt, hash_password, hash_token, verify_password
from app.utils.response import envelope, request_id_from_request

router = APIRouter(prefix="/auth", tags=["admin"])


class LoginRequest(BaseModel):
    username: str
    password: str
    tenant_id: int = 1
    platform: str = "admin"


class RegisterRequest(BaseModel):
    username: str
    password: str
    mobile: str = ""
    email: str = ""
    nickname: str = ""


class RefreshRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class ResetPasswordRequest(BaseModel):
    user_id: int


def _read_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(401, "missing authorization header")
    prefix = "bearer "
    if not authorization.lower().startswith(prefix):
        raise HTTPException(401, "invalid authorization header")
    token = authorization[len(prefix):].strip()
    if not token:
        raise HTTPException(401, "empty token")
    return token


async def _current_user(
    session: AsyncSession,
    authorization: str | None,
):
    access_token = _read_bearer_token(authorization)
    try:
        claims = decode_jwt(access_token)
    except jwt.InvalidTokenError as exc:
        raise HTTPException(401, str(exc)) from None
    if claims.get("type") != "access":
        raise HTTPException(401, "invalid token type")
    user_id = int(claims.get("sub", 0))
    row = await user_crud.get_user(session, user_id)
    if not row:
        raise HTTPException(401, "user not found")
    return row


async def _issue_token_pair(
    request: Request,
    session: AsyncSession,
    *,
    user_id: int,
    tenant_id: int,
    login_type: str = "password",
    platform: str = "admin",
):
    access_token, _, _ = create_jwt(
        subject=str(user_id),
        tid=str(tenant_id),
        token_type="access",
        expires_in=settings.access_token_expire_seconds,
    )
    refresh_token, refresh_jti, refresh_exp = create_jwt(
        subject=str(user_id),
        tid=str(tenant_id),
        token_type="refresh",
        expires_in=settings.refresh_token_expire_seconds,
    )
    await user_token_crud.create_user_token(
        session,
        tenant_id=tenant_id,
        user_id=user_id,
        login_type=login_type,
        jti=refresh_jti,
        refresh_token_hash=hash_token(refresh_token),
        expires_at=datetime.fromtimestamp(refresh_exp, tz=UTC),
        platform=platform,
        user_agent=request.headers.get("user-agent", ""),
        ip=request.client.host if request.client else "",
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_seconds,
    }


@router.post("/login")
async def admin_login(body: LoginRequest, request: Request, session: AsyncSession = Depends(get_session)):
    user = await user_crud.get_user_by_account(session, body.username)
    if not user or not verify_password(body.password, user.password):
        raise HTTPException(401, "invalid account or password")
    data = await _issue_token_pair(
        request,
        session,
        user_id=user.id,
        tenant_id=1,
        login_type="password",
        platform=body.platform,
    )
    return envelope(data=data, request_id=request_id_from_request(request))


@router.post("/register")
async def admin_register(body: RegisterRequest, request: Request, session: AsyncSession = Depends(get_session)):
    exists = await user_crud.get_user_by_account(session, body.username)
    if exists:
        raise HTTPException(409, "username already exists")
    user = await user_crud.create_user(
        session,
        UserCreate(
            username=body.username,
            password=hash_password(body.password),
            mobile=body.mobile,
            email=body.email,
            nickname=body.nickname or body.username,
            avatar="",
            gender=0,
            birthday=None,
        ),
    )
    data = UserOut.model_validate(user).model_dump()
    return envelope(data=data, request_id=request_id_from_request(request))


@router.post("/refresh")
async def admin_refresh(body: RefreshRequest, request: Request, session: AsyncSession = Depends(get_session)):
    try:
        claims = decode_jwt(body.refresh_token)
    except jwt.InvalidTokenError as exc:
        raise HTTPException(401, str(exc)) from None
    if claims.get("type") != "refresh":
        raise HTTPException(401, "invalid token type")
    jti = str(claims.get("jti", ""))
    user_id = int(claims.get("sub", 0))
    token_row = await user_token_crud.get_active_user_token_by_jti(session, jti)
    if not token_row:
        raise HTTPException(401, "token revoked")
    if token_row.refresh_token_hash != hash_token(body.refresh_token):
        raise HTTPException(401, "invalid refresh token")
    data = await _issue_token_pair(
        request,
        session,
        user_id=user_id,
        tenant_id=token_row.tenant_id,
        login_type=token_row.login_type or "password",
        platform=token_row.platform or "admin",
    )
    await user_token_crud.revoke_user_token(session, token_row)
    return envelope(data=data, request_id=request_id_from_request(request))


@router.post("/logout")
async def admin_logout(
    request: Request,
    session: AsyncSession = Depends(get_session),
    authorization: str | None = Header(default=None),
):
    access_token = _read_bearer_token(authorization)
    try:
        claims = decode_jwt(access_token)
    except jwt.InvalidTokenError as exc:
        return envelope(data={"ok": True}, request_id=request_id_from_request(request))
    user_id = int(claims.get("sub", 0))
    await user_token_crud.revoke_active_tokens_by_user(session, user_id)
    return envelope(data={"ok": True}, request_id=request_id_from_request(request))


@router.get("/me", response_model=Envelope[UserOut])
async def admin_me(
    request: Request,
    session: AsyncSession = Depends(get_session),
    authorization: str | None = Header(default=None),
):
    user = await _current_user(session, authorization)
    return envelope(data=UserOut.model_validate(user).model_dump(), request_id=request_id_from_request(request))


@router.post("/change-password")
async def admin_change_password(
    body: ChangePasswordRequest,
    request: Request,
    session: AsyncSession = Depends(get_session),
    authorization: str | None = Header(default=None),
):
    user = await _current_user(session, authorization)
    if not verify_password(body.old_password, user.password):
        raise HTTPException(400, "old password invalid")
    user.password = hash_password(body.new_password)
    await session.commit()
    await user_token_crud.revoke_active_tokens_by_user(session, user.id)
    return envelope(data={"ok": True}, request_id=request_id_from_request(request))


@router.post("/reset-password")
async def admin_reset_password(body: ResetPasswordRequest, request: Request, session: AsyncSession = Depends(get_session)):
    user = await user_crud.get_user(session, body.user_id)
    if not user:
        raise HTTPException(404, "user not found")
    user.password = hash_password("123456")
    await session.flush()
    await user_token_crud.revoke_active_tokens_by_user(session, user.id)
    return envelope(data={"user_id": user.id, "reset_password": "123456"}, request_id=request_id_from_request(request))
