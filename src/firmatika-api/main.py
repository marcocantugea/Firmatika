from fastapi import FastAPI
from routes import auth
from routes import documents
from routes import users_profiles as users
from routes import firmantes
from routes import constancias
from middleware.session_validator import SessionValidatorMiddleware


app = FastAPI()

app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(users.router)
app.include_router(firmantes.router)
app.include_router(constancias.router)
app.add_middleware(SessionValidatorMiddleware)