from pydantic import BaseModel

class Constancia(BaseModel):
    uuid: str
    emitido: str  # contenido de la constancia en formato texto o HTML
    fecha_emision: str  # fecha de emisión de la constancia
    url_blockchain: str  # URL al registro en blockchain
    utr_constancia: str  # UTR (Unique Transaction Reference) de la constancia
    certificado_constancia: str  # certificado digital de la constancia