from pydantic import BaseModel

class UserBasicInfo(BaseModel):
    uuid: str
    nombres: str
    apellidos: str
    email: str
    wallet_address: str