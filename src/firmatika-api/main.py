from fastapi import FastAPI
from routes import auth
from middleware.session_validator import SessionValidatorMiddleware


app = FastAPI()

app.include_router(auth.router)
app.add_middleware(SessionValidatorMiddleware)