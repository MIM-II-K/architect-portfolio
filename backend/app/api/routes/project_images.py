from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.core.auth import require_admin

from app.api.dependencies import (
    get_project_image_service,
)
from app.schemas.project_image import (
    ProjectImageCreate,
    ProjectImageListResponse,
    ProjectImageResponse,
)
from app.services.project_image_service import (
    ProjectImageService,
)


router = APIRouter(
    prefix="/admin/projects",
    tags=["Project Images"],
    dependencies=[Depends(require_admin)],
)


@router.get(
    "/{project_id}/images",
    response_model=ProjectImageListResponse,
)
async def list_images(
    project_id: str,
    service: ProjectImageService = Depends(
        get_project_image_service
    ),
):
    try:
        images = service.list_images(project_id)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return {
        "images": images,
        "total": len(images),
    }


@router.post(
    "/{project_id}/images",
    response_model=ProjectImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_image(
    project_id: str,
    payload: ProjectImageCreate,
    service: ProjectImageService = Depends(
        get_project_image_service
    ),
):
    try:
        return service.create_image(
            project_id,
            payload.model_dump(),
        )
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{project_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_image(
    project_id: str,
    image_id: str,
    service: ProjectImageService = Depends(
        get_project_image_service
    ),
):
    deleted = service.delete_image(
        project_id,
        image_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found.",
        )