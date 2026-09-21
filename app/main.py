from fastapi import FastAPI
from app.api.auth import register, login, profile, logout
from app.api.users import user_crud

app = FastAPI()

app.include_router(register.router, prefix="/api/auth")
app.include_router(login.router, prefix="/api/auth")
app.include_router(profile.router, prefix="/api/auth")
app.include_router(logout.router, prefix="/api/auth")

app.include_router(user_crud.router, prefix="/api")