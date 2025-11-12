from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserSessionToken(BaseModel):
    token: str
    user_uuid: str
    created_at: datetime = datetime.utcnow()
    expires_at: Optional[datetime] = None