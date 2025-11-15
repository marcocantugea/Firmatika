from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models.documentoFirmado import BlockchainTx

class Firmante(BaseModel):
    uuid: str
    documento_uuid: str
    solicitante_uuid: str
    nombres: str
    apellidos: str
    email: str
    wallet: Optional[str] = None  # si tiene wallet
    firma_delegada: bool = False  # true si Firmatika firma por él
    firmado: bool = False
    fecha_firma: Optional[datetime] = None
    tx_hash: Optional[BlockchainTx] = None  # si firmó en blockchain
    metodo_verificacion: Optional[str] = None  # ej: "wallet", "delegada", "biometría"
    codigo_verificacion: Optional[str] = None  # código enviado por email para verificar identidad
    token_verificacion: Optional[str] = None  # token temporal para verificar identidad
    acceso_verificado: bool = False  # si ya se verificó identidad
