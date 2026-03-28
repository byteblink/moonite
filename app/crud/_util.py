from datetime import UTC, datetime
from typing import Any


def apply_updates(obj: Any, payload: dict[str, Any]) -> None:
    for key, value in payload.items():
        if value is not None:
            setattr(obj, key, value)


def soft_delete_mark(obj: Any) -> None:
    obj.is_deleted = True
    obj.deleted_at = datetime.now(UTC)
