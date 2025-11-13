from fastapi import FastAPI
from routes import auth
from routes import documents
from middleware.session_validator import SessionValidatorMiddleware


app = FastAPI()

app.include_router(auth.router)
app.include_router(documents.router)
app.add_middleware(SessionValidatorMiddleware)