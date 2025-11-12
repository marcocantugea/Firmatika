
from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    password: constr(min_length=8, max_length=24)