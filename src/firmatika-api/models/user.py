from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class User(BaseModel):
    uuid: Optional[str] = None
    nombre: str
    apellido: str
    email: EmailStr
    password: str
    verificado: bool = False
    fecha_registro: Optional[datetime] = None
    wallet: Optional[str] = None
    codigo_verificacion: Optional[str] = None
    posible_duplicate_account: Optional[bool] = False
    