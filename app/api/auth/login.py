from fastapi import APIRouter, HTTPException
import bcrypt
from app.utils.rsa import decrypt_password
from app.utils.jwt import sign_token
from app.db.mysql import db

router = APIRouter()


def resolve_login_password(raw_password):
    if raw_password is None:
        raise HTTPException(status_code=400, detail="Password is required")

    try:
        return decrypt_password(raw_password)
    except (TypeError, ValueError):
        return str(raw_password)


@router.post("/login")
def login(data: dict):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (data["email"],))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    decrypted = resolve_login_password(data.get("password"))

    if not bcrypt.checkpw(decrypted.encode(), user["password"].encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        },
        "access_token": sign_token(user),
        "token_type": "Bearer"
    }