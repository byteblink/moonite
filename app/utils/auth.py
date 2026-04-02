import base64
import hashlib
import hmac
import json
import time
import uuid
from typing import Any

from app.core.config import settings


def hash_password(password: str) -> str:
    raw = f"{settings.jwt_secret}:{password}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password), password_hash)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(message: str, secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).digest()
    return _b64url_encode(digest)


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
    header = {"alg": "HS256", "typ": "JWT"}
    header_part = _b64url_encode(json.dumps(header, separators=(",", ":"), ensure_ascii=True).encode("utf-8"))
    payload_part = _b64url_encode(json.dumps(claims, separators=(",", ":"), ensure_ascii=True).encode("utf-8"))
    message = f"{header_part}.{payload_part}"
    token = f"{message}.{_sign(message, settings.jwt_secret)}"
    return token, claims["jti"], exp


def decode_jwt(token: str) -> dict[str, Any]:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("invalid token")
    message = f"{parts[0]}.{parts[1]}"
    expected = _sign(message, settings.jwt_secret)
    if not hmac.compare_digest(parts[2], expected):
        raise ValueError("invalid signature")
    claims = json.loads(_b64url_decode(parts[1]))
    exp = int(claims.get("exp", 0))
    if exp <= int(time.time()):
        raise ValueError("token expired")
    return claims
