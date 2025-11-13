import os
import firebase_admin
from firebase_admin import credentials, firestore
from models.user import User
from dotenv import load_dotenv
from models.documentoFirmado import DocumentoFirmado

load_dotenv()

if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_signed_document(document: DocumentoFirmado):
    doc_ref = db.collection("documentos_firmados").document(document.uuid)
    doc_ref.set(document.dict())

def get_signed_document_by_id(document_id: str) -> DocumentoFirmado | None:
    doc_ref = db.collection("documentos_firmados").document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        return DocumentoFirmado(**data)
    return None

def update_signed_document_upload_info(document_id: str, hash_documento: str, gcs_path: dict[str, str]):
    doc_ref = db.collection("documentos_firmados").document(document_id)
    doc_ref.update({
        "hash_documento": hash_documento,
        "gcs_path": gcs_path,
        "fecha_subida": firestore.SERVER_TIMESTAMP
    })

def update_signed_document_blockchain_info(document_id: str, blockchain_tx: dict):
    doc_ref = db.collection("documentos_firmados").document(document_id)
    doc_ref.update({
        "blockchain_tx": blockchain_tx
    })

def delete_signed_document(document_id: str):
    doc_ref = db.collection("documentos_firmados").document(document_id)
    doc_ref.delete()

def list_signed_documents_by_user(user_id: str) -> list[DocumentoFirmado]:
    documentos_ref = db.collection("documentos_firmados")
    query = documentos_ref.where("user_uuid", "==", user_id)
    results = query.stream()
    documentos = []
    for doc in results:
        data = doc.to_dict()
        documentos.append(DocumentoFirmado(**data))
    return documentos

def verify_signed_document_duplicate(title: str, user_id: str, hash_documento: str) -> bool:
    documentos_ref = db.collection("documentos_firmados")
    query = documentos_ref.where("hash", "==", hash_documento).where("user_uuid", "==", user_id).limit(1)
    results = query.stream()
    return any(True for _ in results)

def log_signed_document_action(document_id: str, action: str, timestamp: str):
    log_entry = {
        "document_id": document_id,
        "action": action,
        "timestamp": timestamp
    }
    db.collection("documento_firmado_logs").add(log_entry)
    return log_entry