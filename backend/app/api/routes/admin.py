from fastapi import APIRouter


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/inquiries")
async def list_inquiries():
    return {
        "message": "Admin inquiry endpoint",
    }