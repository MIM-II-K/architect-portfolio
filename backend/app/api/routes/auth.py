from fastapi import APIRouter, Depends

from app.core.auth import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get("/me")
async def get_me(
    current_user: dict = Depends(get_current_user),
):
    return {
        "uid": current_user.get("uid"),
        "email": current_user.get("email"),
        "admin": current_user.get("admin", False),
    }