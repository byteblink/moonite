import base64
import hashlib
import hmac
import json
import time
import uuid
from typing import Any

import jwt

from app.core.config import settings

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


# def hash_password(password: str) -> str:
#     raw = f"{settings.jwt_secret}:{password}".encode("utf-8")
#     return hashlib.sha256(raw).hexdigest()


# def verify_password(password: str, password_hash: str) -> bool:
#     return hmac.compare_digest(hash_password(password), password_hash)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_jwt(*, subject: str, token_type: str, expires_in: int, jti: str | None = None) -> tuple[str, str, int]:
    now = int(time.time())
    exp = now + expires_in
    claims = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": exp,
        "jti": jti or str(uuid.uuid4()),
    }
    token = jwt.encode(claims, settings.jwt_secret, algorithm="HS256")
    return token, claims["jti"], exp


def decode_jwt(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
