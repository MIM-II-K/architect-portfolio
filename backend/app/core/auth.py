import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# --- INITIALIZE FIREBASE ADMIN SDK ---
if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-key.json")
    
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        raise RuntimeError(
            f"Firebase credentials file not found at path: {os.path.abspath(cred_path)}"
        )

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials

    try:
        decoded_token = auth.verify_id_token(token)
    except Exception as exc:
        print(f"\n🔥 FIREBASE ERROR DETAILS: {str(exc)}\n")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(exc)}",
        ) from exc

    return decoded_token


def require_admin(
    current_user: dict = Depends(get_current_user),
) -> dict:
    if current_user.get("admin") is not True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    return current_user