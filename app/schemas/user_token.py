from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserTokenOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    user_id: int
    login_type: str = ""
    jti: str = ""
    refresh_token_hash: str = ""
    expires_at: datetime
    platform: str = ""
    user_agent: str = ""
    ip: str = ""
    is_revoked: bool
    revoked_at: Optional[datetime] = None
    is_deleted: bool
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
