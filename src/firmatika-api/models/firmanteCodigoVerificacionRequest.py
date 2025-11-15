from pydantic import BaseModel

class FirmanteCodigoVerificacionRequest(BaseModel):
    codigo_verificacion: str