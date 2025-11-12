import uuid
from datetime import datetime, timedelta
from models.userSessionToken import UserSessionToken
from services.firestore import db
from fastapi import HTTPException
from datetime import datetime


SESSION_DURATION_MINUTES = 30

def crear_token_sesion(user_uuid: str) -> UserSessionToken:
    token = str(uuid.uuid4())
    now = datetime.utcnow()
    expires = now + timedelta(minutes=SESSION_DURATION_MINUTES)

    session = UserSessionToken(
        token=token,
        user_uuid=user_uuid,
        created_at=now,
        expires_at=expires
    )

    db.collection("sesiones").document(token).set(session.dict())
    return session

def renovar_token_sesion(token: str) -> UserSessionToken:
    doc_ref = db.collection("sesiones").document(token)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Token no encontrado")

    data = doc.to_dict()
    now = datetime.utcnow()

    expires_at = data["expires_at"]

    if expires_at.tzinfo is not None:
        expires_at = expires_at.replace(tzinfo=None)

    if expires_at < now:
        raise HTTPException(status_code=401, detail="Token expirado")

    nuevo_token = crear_token_sesion(data["user_uuid"])
    doc_ref.delete()
    return nuevo_token

