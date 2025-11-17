from pydantic import BaseModel
from typing import List,Optional
from models.documentoFirmado import DocumentoFirmado
from models.firmante import Firmante
from models.constancia import Constancia
from models.userInfo import UserBasicInfo

class ConstanciaDocumento(BaseModel):
    documento: DocumentoFirmado
    hash: str
    usuario_documento: UserBasicInfo
    firmas: Optional[List[Firmante]] = None
    constancia: Constancia