from pydantic import BaseModel

class FirmanteFirmarRequest(BaseModel):
    metodo_verificacion: str