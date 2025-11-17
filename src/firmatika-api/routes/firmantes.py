import uuid
import hashlib
import random
from datetime import datetime, timedelta
from fastapi import APIRouter, Body, File,HTTPException,Request, UploadFile
from models.firmanteRequest import FirmanteRequest
from models.firmante import Firmante
from models.firmanteFirmarRequest import FirmanteFirmarRequest
from services.firmantes import add_firmante_to_document,valida_token_verificacion,actualizar_firmante,get_firmante_by_email,get_firmante_by_uuid,actualizar_firmante_wallet,acutializar_firmante_biometrica,get_documentos_by_firmante_uuid,get_documento_by_firmante_uuid
from models.firmanteCodigoVerificacionRequest import FirmanteCodigoVerificacionRequest
from services.session import crear_token_sesion,renovar_token_sesion,token_session_exists
from services.blockchain import firmar_hash_en_blockchain, wallet_existe_en_red
from services.documents import get_document_by_uuid, log_signed_document_action

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

    if not firmante:
        raise HTTPException(status_code=404, detail="Token de verificación inválido")

    if firmante.acceso_verificado:
        return {"message": "Firmante ya verificado previamente, solicite un nuevo código si es necesario"}

    if firmante.codigo_verificacion != codigo_verificacion_request.codigo_verificacion:
        raise HTTPException(status_code=400, detail="Código de verificación incorrecto")
    
    firmante.acceso_verificado = True

    actualizar_firmante(firmante)
    token=""
    token_session=token_session_exists(firmante.uuid)
    if not token_session:
        token = crear_token_sesion(firmante.uuid)
    else:
        token = renovar_token_sesion(firmante.uuid)

    return {"message": "Firmante verificado exitosamente", "firmante_uuid": firmante.uuid, "token": token.token}

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
    return {"message": "Código de verificación reenviado exitosamente", "firmante_uuid": firmante.uuid}

@router.patch("/firmantes/wallet/{firmante_uuid}")
async def actualizar_wallet_firmante(firmante_uuid: str, wallet_address: str = Body(..., embed=True)):
    firmante = get_firmante_by_uuid(firmante_uuid)

    if not firmante:
        raise HTTPException(status_code=404, detail="Firmante no encontrado")

    if not wallet_existe_en_red(wallet_address):
        raise HTTPException(status_code=400, detail="La dirección de wallet proporcionada no existe en la red blockchain")

    firmante.wallet = wallet_address
    try:
        actualizar_firmante_wallet(firmante_uuid, wallet_address)
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    return {"message": "Wallet del firmante actualizada exitosamente"}

@router.patch("/firmantes/biometrica/{firmante_uuid}")
async def actualizar_biometrica_firmante(firmante_uuid: str, biometric_data: dict = Body(...)):
    firmante = get_firmante_by_uuid(firmante_uuid)

    if not firmante:
        raise HTTPException(status_code=404, detail="Firmante no encontrado")

    firmante.biometric_data = biometric_data

    try:
        acutializar_firmante_biometrica(firmante_uuid, biometric_data)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    return {"message": "Datos biométricos del firmante actualizados exitosamente"}


@router.post("/firmantes/firmar/{documento_uuid}")
def firmar_documento(documento_uuid: str, firmante_firmar_request: FirmanteFirmarRequest = Body(...)):

    firmante = get_documento_by_firmante_uuid(firmante_firmar_request.firmante_uuid, documento_uuid)

    if not firmante:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    documento= get_document_by_uuid(documento_uuid)

    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado en sistema")
    
    nombre_completo=f"{firmante.nombres} {firmante.apellidos}"
    if(firmante.firma_delegada):
       #logica para firma delegada
        print("firma delegada")
        print("Firmando documento en blockchain...")
        print("Hash del documento:", documento.hash_documento)
        blockchain_tx_hash = firmar_hash_en_blockchain(documento.hash_documento,nombre_completo, documento.nombre, documento.descripcion, True, firmante.wallet)
        firmante.metodo_verificacion=firmante_firmar_request.metodo_verificacion
        firmante.tx_hash=blockchain_tx_hash
        firmante.firmado=True
        firmante.fecha_firma=datetime.utcnow()
        actualizar_firmante(firmante)

        log_signed_document_action(documento.uuid, "signed by user_uuid"+firmante.uuid+" firma delegada", datetime.utcnow().isoformat())

        
    else:
       #logica para firma con wallet
        print("firma delegada false")
        print("Firmando documento en blockchain...")
        print("Hash del documento:", documento.hash_documento)
        
        blockchain_tx_hash = firmar_hash_en_blockchain(documento.hash_documento,nombre_completo, documento.nombre, documento.descripcion, False)
        firmante.metodo_verificacion=firmante_firmar_request.metodo_verificacion
        firmante.tx_hash=blockchain_tx_hash
        firmante.firmado=True
        firmante.fecha_firma=datetime.utcnow()
        actualizar_firmante(firmante)

        log_signed_document_action(documento.uuid, "signed by user_uuid"+firmante.uuid+" by system", datetime.utcnow().isoformat())


    # Lógica para firmar el documento según el método de verificación
    return {"message": f"Documento {firmante.documento_uuid} firmado usando {firmante_firmar_request.metodo_verificacion}"}