from pydantic import BaseModel
from typing import Optional

class UserBasicInfo(BaseModel):
    uuid: str
    nombres: str
    apellidos: str
    email: str
    wallet_address: Optional[str] = None