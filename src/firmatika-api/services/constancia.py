import os
import firebase_admin
from firebase_admin import credentials, firestore
from models.user import User
from dotenv import load_dotenv
from models.documentoFirmado import DocumentoFirmado
from models.documentoFirmado import BlockchainTx
from models.constanciaDocumento import ConstanciaDocumento
from models.constancia import Constancia
from models.userInfo import UserBasicInfo
from services.certificate import generar_certificado
from services.documents import get_document_by_uuid,get_firmantes_by_document_uuid
from services.users import get_user_by_id
from services.blockchain import get_url_transaction_blockchain

load_dotenv()

if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    firebase_admin.initialize_app(cred)

db = firestore.client()

def create_constancia_documento(document_uuid: str) -> ConstanciaDocumento:
    # Obtener el documento firmado
    documento = get_document_by_uuid(document_uuid)
    if not documento:
        raise ValueError("Documento no encontrado")

    # Obtener el usuario que firmó el documento
    usuario_documento = get_user_by_id(documento.user_uuid)
    if not usuario_documento:
        raise ValueError("Usuario no encontrado")

    # Obtener los firmantes del documento
    firmas = get_firmantes_by_document_uuid(document_uuid)

    # validamos que todos los firmantes hayan firmado
    valido=all([f["firmado"] for f in firmas])
    if not valido:
        raise ValueError("No todos los firmantes han firmado el documento")

    # Generar el certificado digital de la constancia
    certificado_constancia = generar_certificado(documento)

    # Crear la constancia
    constancia = Constancia(
        uuid=documento.uuid,
        emitido=f"Constancia de firma para el documento {documento.nombre}",
        fecha_emision=documento.fecha_subida.isoformat(),
        url_blockchain=get_url_transaction_blockchain(documento.blockchain_tx.tx_hash) if documento.blockchain_tx else "",
        utr_constancia=os.getenv("HOST_FRONT_URL") + "/constancia/" + documento.uuid+"/verify",
        certificado_constancia=certificado_constancia
    )

    infoUser= UserBasicInfo(
        uuid=usuario_documento.uuid,
        nombres=usuario_documento.nombre,
        apellidos=usuario_documento.apellido,
        email=usuario_documento.email,
        wallet_address=usuario_documento.wallet
    )

    # Crear y retornar el objeto ConstanciaDocumento
    constancia_documento = ConstanciaDocumento(
        documento=documento,
        hash=documento.hash_documento,
        usuario_documento=infoUser,
        firmas=firmas,
        constancia=constancia
    )

    doc_ref = db.collection("constancias").document(constancia_documento.constancia.uuid)
    doc_ref.set(constancia_documento.dict())

    return constancia_documento


def get_constancia_documento_by_uuid(constancia_uuid: str) -> ConstanciaDocumento:
    doc_ref = db.collection("constancias").document(constancia_uuid)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        constancia_documento = ConstanciaDocumento(**data)
        return constancia_documento
    else:
        raise ValueError("Constancia no encontrada")
    
def exist_constancia_documento(constancia_uuid: str) -> bool:
    doc_ref = db.collection("constancias").document(constancia_uuid)
    doc = doc_ref.get()
    return doc.exists