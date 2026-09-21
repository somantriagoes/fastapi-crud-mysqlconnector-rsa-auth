from fastapi import APIRouter, Depends
from app.middleware.auth import auth_required

router = APIRouter()

@router.get("/profile")
def profile(user=Depends(auth_required)):
    return user