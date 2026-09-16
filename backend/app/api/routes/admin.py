from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.api.dependencies import get_project_service
from app.schemas.project import ProjectResponse
from app.schemas.project_admin import (
    ProjectCreate,
    ProjectUpdate,
)
from app.services.project_service import ProjectService

from app.api.dependencies import get_category_service
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import CategoryService


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    payload: ProjectCreate,
    service: ProjectService = Depends(
        get_project_service
    ),
):
    try:
        return service.create_project(
            payload.model_dump()
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.patch(
    "/projects/{project_id}",
    response_model=ProjectResponse,
)
async def update_project(
    project_id: str,
    payload: ProjectUpdate,
    service: ProjectService = Depends(
        get_project_service
    ),
):
    update_data = payload.model_dump(
        exclude_unset=True
    )

    try:
        project = service.update_project(
            project_id,
            update_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: str,
    service: ProjectService = Depends(
        get_project_service
    ),
):
    deleted = service.delete_project(project_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )


@router.get("/inquiries")
async def list_inquiries():
    return {
        "message": "Admin inquiry endpoint",
    }

@router.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    payload: CategoryCreate,
    service: CategoryService = Depends(
        get_category_service
    ),
):
    try:
        return service.create_category(
            payload.model_dump()
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.patch(
    "/categories/{category_id}",
    response_model=CategoryResponse,
)
async def update_category(
    category_id: str,
    payload: CategoryUpdate,
    service: CategoryService = Depends(
        get_category_service
    ),
):
    try:
        category = service.update_category(
            category_id,
            payload.model_dump(
                exclude_unset=True
            ),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return category


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    category_id: str,
    service: CategoryService = Depends(
        get_category_service
    ),
):
    deleted = service.delete_category(category_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )  