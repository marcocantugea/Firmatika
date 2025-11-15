import uuid
import hashlib
import random
from datetime import datetime, timedelta
from fastapi import APIRouter, Body, File,HTTPException,Request, UploadFile
from models.firmanteRequest import FirmanteRequest
from models.firmante import Firmante
from services.firmantes import add_firmante_to_document,valida_token_verificacion,actualizar_firmante,get_firmante_by_email
from models.firmanteCodigoVerificacionRequest import FirmanteCodigoVerificacionRequest

router = APIRouter()

@router.post("/firmantes/{document_uuid}/agregar")
async def add_firmante(document_uuid: str, firmante_request: FirmanteRequest = Body(...)):
    try:
        firmante_uuid = str(uuid.uuid4())
        firmante = Firmante(
            uuid=firmante_uuid,
            documento_uuid=document_uuid,
            solicitante_uuid=firmante_request.soliciante_uuid,
            nombres=firmante_request.nombres,
            apellidos=firmante_request.apellidos,
            email=firmante_request.email,
            codigo_verificacion=str(random.randint(100000, 999999)),
            token_verificacion=str(uuid.uuid4()),
            verificado=False,
        )
        add_firmante_to_document(document_uuid, firmante_request.soliciante_uuid, firmante)
        return {"message": "Firmante agregado exitosamente", "firmante_uuid": firmante_uuid}
    except ValueError as ve:
        print("value error")
        print(str(ve))
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print("exception")
        print(str(e))
        print ("stack trace")
        print (e.__traceback__)
        raise HTTPException(status_code=500, detail="Error al agregar firmante")
    
@router.post("/firmantes/verificar/{token}")
async def verificar_firmante(token: str,codigo_verificacion_request: FirmanteCodigoVerificacionRequest = Body(...)):
    firmante = valida_token_verificacion(token)

    if firmante.acceso_verificado:
        return {"message": "Firmante ya verificado previamente, solicite un nuevo código si es necesario"}

    if not firmante:
        raise HTTPException(status_code=404, detail="Token de verificación inválido")
    
    if firmante.codigo_verificacion != codigo_verificacion_request.codigo_verificacion:
        raise HTTPException(status_code=400, detail="Código de verificación incorrecto")
    
    firmante.acceso_verificado = True

    actualizar_firmante(firmante)

    return {"message": "Firmante verificado exitosamente"}

@router.post("/firmantes/reenviar_codigo")
async def reenviar_codigo_verificacion(firmanteRequest: FirmanteRequest = Body(...)):
    firmante = get_firmante_by_email(firmanteRequest.email)

    if not firmante:
        raise HTTPException(status_code=404, detail="Firmante no encontrado")

    if not firmante.acceso_verificado:
        return {"message": "Firmante no ha verificado su identidad aún, no se puede reenviar código"}

    firmante.codigo_verificacion = str(random.randint(100000, 999999))
    firmante.token_verificacion = str(uuid.uuid4())
    firmante.acceso_verificado = False

    actualizar_firmante(firmante)

    from services.email import enviar_codigo_verificacion
    enviar_codigo_verificacion(firmante.email, firmante.codigo_verificacion, "http://127.0.0.1:8000/firmantes/verificar/"+firmante.token_verificacion)
    return {"message": "Código de verificación reenviado exitosamente"}