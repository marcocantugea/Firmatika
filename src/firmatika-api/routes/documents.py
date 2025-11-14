import uuid
import hashlib
from datetime import datetime, timedelta
from fastapi import APIRouter, Body, File,HTTPException,Request, UploadFile
from models.documentoFirmado import DocumentoFirmado
from services.documents import list_signed_documents_by_user, update_signed_document_blockchain_info,verify_signed_document_duplicate,save_signed_document,log_signed_document_action,update_signed_document_upload_info,get_signed_document_by_id
from services.gsc import subir_pdf_a_gcs, generar_url_firmada
from services.blockchain import firmar_hash_en_blockchain

router = APIRouter()

@router.get("/documentos/{user_id}")
def get_user_documents(user_id: str):
    documents = list_signed_documents_by_user(user_id)
    return {"user_id": user_id, "documents": documents}

@router.post("/documentos/{user_id}")
def add_user_document(user_id: str, payload: dict = Body(...)):
    documento = DocumentoFirmado(
        uuid=str(uuid.uuid4()),
        user_uuid=user_id,
        tipo=payload["tipo"],
        nombre=payload["nombre"],
        descripcion=payload.get("descripcion"),
        hash_documento=None,
        gcs_path=None,
        blockchain_tx=None
    )

    if verify_signed_document_duplicate(documento.nombre, user_id, documento.hash_documento):
        raise HTTPException(status_code=400, detail="Documento duplicado")
    
    save_signed_document(documento)
    log_signed_document_action(documento.uuid, "created", datetime.utcnow().isoformat())
    return {"message": "Documento agregado", "documento": documento}

@router.post("/documentos/{document_id}/archivo")
async def subir_archivo_documento(document_id: str, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    contenido = await file.read()
    hash_documento = hashlib.sha256(contenido).hexdigest()

    gcs_path = subir_pdf_a_gcs(document_id, contenido)

    update_signed_document_upload_info(document_id, hash_documento, gcs_path)
    log_signed_document_action(document_id, "file_uploaded", datetime.utcnow().isoformat())

    return {"success": True, "mensaje": "Archivo subido", "hash": hash_documento, "gcs_path": gcs_path}

@router.post("/documentos/{document_id}/blockchain")
def registrar_en_blockchain(document_id: str):
    document = get_signed_document_by_id(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    data = document.dict()
    hash_documento = data.get("hash_documento")
    if not hash_documento:
        raise HTTPException(status_code=400, detail="Documento aún no tiene hash")

    # Aquí iría tu lógica de firma en blockchain
    #mock resoltado de la transacción
    #blockchain_tx_hash = f"0x{hashlib.sha256(f'{document_id}{hash_documento}{datetime.utcnow().timestamp()}'.encode()).hexdigest()}"
    blockchain_tx_hash = firmar_hash_en_blockchain(hash_documento)
    update_signed_document_blockchain_info(document_id, blockchain_tx_hash)
    log_signed_document_action(document_id, "registered_on_blockchain", datetime.utcnow().isoformat())

    return {"mensaje": "Documento registrado en blockchain", "tx": blockchain_tx_hash}

@router.get("/documentos/{document_id}/url")
def obtener_url_documento(document_id: str):
    document = get_signed_document_by_id(document_id)
    if not document or not document.gcs_path:
        raise HTTPException(status_code=404, detail="Documento no encontrado o sin archivo asociado")

    gcs_path = generar_url_firmada(document_id)
    log_signed_document_action(document_id, "url_generated", datetime.utcnow().isoformat())
    return {"document_id": document_id, "gcs_path": gcs_path}