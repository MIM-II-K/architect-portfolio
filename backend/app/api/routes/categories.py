from fastapi import APIRouter


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get("")
async def list_categories():
    return {
        "message": "Category listing endpoint",
    }