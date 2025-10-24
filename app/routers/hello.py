from fastapi import APIRouter

router = APIRouter(prefix="/hello", tags=["hello"])

@router.get("/")
def say_hello():
    return {"message": "Hello depuis FastAPI 👋"}
