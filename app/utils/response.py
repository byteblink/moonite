import time
import uuid
from typing import Any

from fastapi import Request


def envelope(
    *,
    code: int = 0,
    message: str = "success",
    data: Any = None,
    request_id: str | None = None,
) -> dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
        "request_id": request_id or str(uuid.uuid4()),
    }


def request_id_from_request(request: Request) -> str:
    rid = request.headers.get("x-request-id")
    return rid.strip() if rid else str(uuid.uuid4())
