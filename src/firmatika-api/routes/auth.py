import random
import uuid
from fastapi import APIRouter, Body,HTTPException,Request
from httpx import request
from models.user import User
from models.userCreated import UserCreate
from models.tokenRefreshRequest import TokenRefreshRequest
from services.firestore import save_user_to_firestore,verificar_usuario,get_user_by_email,verify_user_duplicate,verify_user_duplicateName,log_user_creation
from datetime import datetime
from services.email import enviar_codigo_verificacion
from passlib.context import CryptContext
from services.session import crear_token_sesion,renovar_token_sesion

router = APIRouter()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password) 

@router.get("/healthcheck")
def health_check():
    return {"status": "ok"}

@router.post("/registro")
def registrar_usuario(user_created: UserCreate, request: Request):
    user= User(
        uuid=str(uuid.uuid4()),
        nombre=user_created.nombre,
        apellido=user_created.apellido,
        email=user_created.email,
        password=hash_password(user_created.password),
        fecha_registro=datetime.utcnow(),
        verificado=False,
        codigo_verificacion=str(random.randint(100000, 999999)),
        wallet=None
    ) 
    userDuplicate = verify_user_duplicate(user.email)
    if userDuplicate:
        raise HTTPException(status_code=400, detail="Usuario ya registrado")
    
    if verify_user_duplicateName(user.nombre, user.apellido):
        user.posible_duplicate_account = True
    
    # Guardar usuario en Firestore
    save_user_to_firestore(user)

    # Registrar información adicional del usuario
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    referral_source = request.headers.get("referer")  # opcional
    additional_info = request.headers.get("x-custom-info")  # si usas headers personalizados

    log_user_creation(
        user_uuid=user.uuid,
        ip_address=ip_address,
        user_agent=user_agent,
        referral_source=referral_source,
        additional_info=additional_info
    )

    log_user_creation(user.uuid, ip_address, user_agent, referral_source, additional_info)

    ## Enviar código de verificación por correo
    enviar_codigo_verificacion(user.email, user.codigo_verificacion)
    return {"mensaje": "Usuario registrado. Se envió un código de verificación al correo."}

@router.post("/verificar")
def verificar_codigo(email: str = Body(...), codigo: str = Body(...)):
    if verificar_usuario(email, codigo):
        return {"mensaje": "Correo verificado correctamente"}
    else:
        raise HTTPException(status_code=400, detail="Código incorrecto o usuario no encontrado")
    
@router.post("/login")
def login(email: str = Body(...), password: str = Body(...)):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    data = user.dict()
    if not data.get("verificado"):
        raise HTTPException(status_code=403, detail="Usuario no verificado")

    hashed_password = data.get("password")
    if not pwd_context.verify(password, hashed_password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")


    session = crear_token_sesion(data.get("uuid"))
    return {"success": True, "token": session.token, "expires_at": session.expires_at,"user_id":user.uuid }

@router.post("/session/refresh")
def refresh_token(request: TokenRefreshRequest):
    try:
        nueva_sesion = renovar_token_sesion(request.token)
        return {
            "mensaje": "Token renovado",
            "token": nueva_sesion.token,
            "expires_at": nueva_sesion.expires_at,
            "user_id": nueva_sesion.user_uuid
        }
    except HTTPException as e:
        raise e
