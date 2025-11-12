from pydantic import BaseModel

class TokenRefreshRequest(BaseModel):
    token: str