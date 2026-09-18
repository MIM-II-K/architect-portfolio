import os
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.core.auth import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY", "")


# --- SCHEMAS ---

class LoginRequest(BaseModel):
    username: EmailStr | str
    password: str


# --- ROUTES ---

@router.get("/me")
async def get_me(
    current_user: dict = Depends(get_current_user),
):
    return {
        "uid": current_user.get("uid"),
        "email": current_user.get("email"),
        "admin": current_user.get("admin", False),
    }


@router.post("/login")
async def login(
    payload: LoginRequest,
):
    if not FIREBASE_WEB_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="FIREBASE_WEB_API_KEY is not configured in environment variables.",
        )

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={
                "email": payload.username,
                "password": payload.password,
                "returnSecureToken": True,
            },
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = response.json()

    return {
        "access_token": data["idToken"],
        "token_type": "bearer",
    }