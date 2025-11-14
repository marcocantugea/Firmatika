from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class BlockchainTx(BaseModel):
    tx_hash: str
    block_number: int
    timestamp: int
    network: str

class DocumentoFirmado(BaseModel):
    uuid: str  # identificador único del documento
    user_uuid: str  # relación con el usuario
    tipo: str  # ej: "contrato", "acuerdo", "certificado"
    nombre: str  # nombre del documento
    descripcion: Optional[str] = None
    hash_documento: Optional[str] = None  # hash SHA256 del archivo PDF
    gcs_path: Optional[Dict[str, str]] = None  # ruta o ID del archivo en Google Cloud Storage
    fecha_subida: Optional[datetime] = None
    fecha_eliminacion: Optional[datetime]=None # fecha programada para eliminación (1 año después)
    blockchain_tx: Optional[BlockchainTx] = None  # info del resultado en blockchain
    