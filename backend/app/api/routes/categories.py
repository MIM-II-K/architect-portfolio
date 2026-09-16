from fastapi import APIRouter, Depends

from app.api.dependencies import get_category_service
from app.schemas.category import CategoryListResponse
from app.services.category_service import CategoryService


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get(
    "",
    response_model=CategoryListResponse,
)
async def list_categories(
    service: CategoryService = Depends(
        get_category_service
    ),
):
    categories = service.list_categories()

    return {
        "categories": categories,
        "total": len(categories),
    }