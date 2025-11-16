import os
import firebase_admin
from firebase_admin import credentials, firestore
from models.user import User
from dotenv import load_dotenv
from models.userCreationLog import UserCreationLog
from passlib.context import CryptContext
from models.firmante import Firmante
from services.users import get_user_by_id
from services.documents import get_document_by_uuid
from services.email import enviar_codigo_verificacion
from services.blockchain import wallet_existe_en_red

load_dotenv()

if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    firebase_admin.initialize_app(cred)

db = firestore.client()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def add_firmante_to_document(document_uuid: str, solicitante_uuid: str,firmante  : Firmante):

    # verificamos si el firmante ya existe para ese documento
    if validate_firmante_duplicate(firmante.email, document_uuid):
        raise ValueError("El firmante ya ha sido agregado a este documento")

    # Verificar que el solicitante existe
    solicitante = get_user_by_id(solicitante_uuid)
    if not solicitante:
     raise ValueError("Solicitante no encontrado")
    
    # Verificar que el documento existe
    documento = get_document_by_uuid(document_uuid)
    if not documento:
     raise ValueError("Documento no encontrado")
    
    # Verificamos si el documento le pertenece al solicitante
    if documento.user_uuid != solicitante_uuid:
        raise ValueError("El solicitante no es el propietario del documento")
    
    doc_ref = db.collection("firmantes").document(firmante.uuid)
    firmante.documento_uuid = document_uuid
    firmante.solicitante_uuid = solicitante_uuid

    enviar_codigo_verificacion(firmante.email, firmante.codigo_verificacion, "http://127.0.0.1:8000/firmantes/verificar/"+firmante.token_verificacion)

    doc_ref.set(firmante.dict())


def validate_firmante_duplicate(email: str, document_uuid: str) -> bool:
    firmantes_ref = db.collection("firmantes")
    query = firmantes_ref.where("email", "==", email).where("documento_uuid", "==", document_uuid).limit(1)
    results = query.stream()
    for _ in results:
        return True
    return False

def valida_token_verificacion(token: str) -> Firmante | None:
    firmantes_ref = db.collection("firmantes")
    query = firmantes_ref.where("token_verificacion", "==", token).limit(1)
    results = query.stream()
    for doc in results:
        data = doc.to_dict()
        return Firmante(**data)
    return None

def actualizar_firmante(firmante: Firmante):

    doc_ref = db.collection("firmantes").document(firmante.uuid)
    doc_ref.update(firmante.dict())

def get_firmante_by_email(email: str) -> Firmante | None:
    firmantes_ref = db.collection("firmantes")
    query = firmantes_ref.where("email", "==", email).limit(1)
    results = query.stream()
    for doc in results:
        data = doc.to_dict()
        return Firmante(**data)
    return None

def get_firmante_by_uuid(firmante_uuid: str) -> Firmante | None:
    doc_ref = db.collection("firmantes").document(firmante_uuid)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        return Firmante(**data)
    return None

def get_documentos_by_firmante_uuid(firmante_uuid: str):
    firmantes_ref = db.collection("firmantes")
    query = firmantes_ref.where("documento_uuid", "==", firmante_uuid)
    results = query.stream()
    documentos = []
    for doc in results:
        data = doc.to_dict()
        documentos.append(data)
    return documentos

def get_documento_by_firmante_uuid(firmante_uuid: str, documento_uuid: str):
    firmantes_ref = db.collection("firmantes")
    query = firmantes_ref.where("documento_uuid", "==", documento_uuid).where("uuid", "==", firmante_uuid).limit(1)
    results = query.stream()
    for doc in results:
        data = doc.to_dict()
        return Firmante(**data)
    return None

def actualizar_firmante_wallet(firmante_uuid: str, wallet_address: str):
    
    if not wallet_existe_en_red(wallet_address):
        raise ValueError("La dirección de wallet proporcionada no existe en la red blockchain")
    
    doc_ref = db.collection("firmantes").document(firmante_uuid)
    doc_ref.update({"wallet": wallet_address,"firma_delegada": False})

def acutializar_firmante_biometrica(firmante_uuid: str, biometric_data: dict[str, str]):
    doc_ref = db.collection("firmantes").document(firmante_uuid)
    doc_ref.update({"biometric_data": biometric_data})


def firmar_documento_blockchain(firmante_uuid: str, tx_hash: str, metodo_verificacion: str):
    doc_ref = db.collection("firmantes").document(firmante_uuid)
    doc_ref.update({
        "firmado": True,
        "fecha_firma": firestore.SERVER_TIMESTAMP,
        "tx_hash": tx_hash,
        "metodo_verificacion": metodo_verificacion
    })

