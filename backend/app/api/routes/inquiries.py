from fastapi import APIRouter


router = APIRouter(
    prefix="/inquiries",
    tags=["Inquiries"],
)


@router.post("")
async def create_inquiry():
    return {
        "message": "Inquiry creation endpoint",
    }