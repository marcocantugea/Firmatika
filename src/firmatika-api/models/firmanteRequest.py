from pydantic import BaseModel

class FirmanteRequest(BaseModel):
    soliciante_uuid: str
    nombres: str
    apellidos: str
    email: str