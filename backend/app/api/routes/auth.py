from fastapi import APIRouter


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
async def login():
    return {
        "message": "Login endpoint",
    }


@router.post("/logout")
async def logout():
    return {
        "message": "Logout endpoint",
    }


@router.post("/refresh")
async def refresh_token():
    return {
        "message": "Refresh endpoint",
    }