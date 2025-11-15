from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from services.firestore import db
from datetime import datetime

class SessionValidatorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Excepciones: rutas públicas
        print( request.url.path )
        if request.url.path in ["/login", "/registro","/verificar", "/healthcheck"] or request.url.path.startswith("/firmantes/verificar") or request.url.path.startswith("/openapi.json"):
            return await call_next(request)

        # Extraer token del header
        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse(status_code=401, content={"detail": "Session inválida o no proporcionada"})

        # Buscar sesión en Firestore
        doc_ref = db.collection("sesiones").document(token)
        doc = doc_ref.get()
        if not doc.exists:
            return JSONResponse(status_code=401, content={"detail": "Session inválida o no encontrada"})

        data = doc.to_dict()
        expires_at = data["expires_at"]
        if expires_at.tzinfo is not None:
            expires_at = expires_at.replace(tzinfo=None)

        if expires_at < datetime.utcnow():
            return JSONResponse(status_code=401, content={"detail": "Token expirado"})

        # Token válido → continuar
        request.state.user_uuid = data["user_uuid"]
        return await call_next(request)