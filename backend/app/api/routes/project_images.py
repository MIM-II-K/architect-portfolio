from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form,
)

from app.core.auth import require_admin
from app.api.dependencies import get_project_image_service
from app.schemas.project_image import (
    ProjectImageListResponse,
    ProjectImageResponse,
)
from app.services.project_image_service import ProjectImageService

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
    service: ProjectImageService = Depends(get_project_image_service),
):
    try:
        return service.list_images(project_id)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "/{project_id}/images",
    response_model=ProjectImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_image(
    project_id: str,
    file: UploadFile = File(...),              # 👈 Accepts the binary file stream
    alt_text: str = Form(None),              # 👈 Accepts form text fields
    caption: str = Form(None),
    service: ProjectImageService = Depends(get_project_image_service),
):
    try:
        # Call the actual async upload service that hits Supabase Storage
        return await service.upload_image(
            project_id=project_id,
            file=file,
            alt_text=alt_text,
            caption=caption,
        )
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image upload failed: {str(exc)}",
        ) from exc


@router.delete(
    "/{project_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_image(
    project_id: str,
    image_id: str,
    service: ProjectImageService = Depends(get_project_image_service),
):
    deleted = service.delete_image(project_id, image_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found.",
        )