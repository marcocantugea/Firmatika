import os
import firebase_admin
from firebase_admin import credentials, firestore
from models.user import User
from dotenv import load_dotenv
from models.userCreationLog import UserCreationLog
from passlib.context import CryptContext

load_dotenv()

if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    firebase_admin.initialize_app(cred)

db = firestore.client()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password) 

def get_user_by_id(user_id: str) -> User | None:
    doc_ref = db.collection("usuarios").where("uuid", "==", user_id)
    docs = doc_ref.get()
    for doc in docs:
        data = doc.to_dict()
        return User(**data)
    return None


def update_user(user: User):
    doc_ref = db.collection("usuarios").document(user.email)
    doc_ref.set(user.dict())

def update_user_password(user_id: str, new_password: str):
    user = get_user_by_id(user_id)
    if user:
        user.password = hash_password(new_password)
        update_user(user)