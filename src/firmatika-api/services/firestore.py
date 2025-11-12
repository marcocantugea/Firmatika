import os
import firebase_admin
from firebase_admin import credentials, firestore
from models.user import User
from dotenv import load_dotenv
from models.userCreationLog import UserCreationLog

load_dotenv()

if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_user_to_firestore(user: User):
    doc_ref = db.collection("usuarios").document(user.email)
    doc_ref.set(user.dict())

def verificar_usuario(email: str, codigo: str):
    doc_ref = db.collection("usuarios").document(email)
    doc = doc_ref.get()
    if not doc.exists:
        return False
    data = doc.to_dict()
    if data.get("codigo_verificacion") == codigo:
        doc_ref.update({"verificado": True, "codigo_verificacion": None})
        return True
    return False

def get_user_by_email(email: str) -> User | None:
    doc_ref = db.collection("usuarios").document(email)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        return User(**data)
    return None

def verify_user_duplicate(email: str) -> bool:
    doc_ref = db.collection("usuarios").document(email)
    doc = doc_ref.get()
    return doc.exists

def verify_user_duplicateName(nombre: str, apellido: str) -> bool:
    usuarios_ref = db.collection("usuarios")
    query = usuarios_ref.where("nombre", "==", nombre).where("apellido", "==", apellido).limit(1)
    results = query.stream()
    return any(True for _ in results)

def log_user_creation(user_uuid: str, ip_address: str = None, user_agent: str = None, referral_source: str = None, additional_info: str = None):
    log_entry = UserCreationLog(
        user_uuid=user_uuid,
        ip_address=ip_address,
        user_agent=user_agent,
        referral_source=referral_source,
        additional_info=additional_info
    )
    db.collection("user_creation_logs").add(log_entry.dict())
    return log_entry