from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreationLog(BaseModel):
    user_uuid: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    referral_source: Optional[str] = None
    additional_info: Optional[str] = None
    timestamp: datetime = datetime.utcnow()
