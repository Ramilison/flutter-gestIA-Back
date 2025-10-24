from fastapi import FastAPI
from app.routes import router
from app.firebase_config import db





app = FastAPI()

app.include_router(router)
