from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from app.api.dependencies import get_storage_service
from app.core.auth import require_admin
from app.services.storage_service import StorageService


router = APIRouter(
    prefix="/admin/uploads",
    tags=["Uploads"],
    dependencies=[Depends(require_admin)],
)


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

MAX_IMAGE_SIZE = 10 * 1024 * 1024


@router.post("/project-image")
async def upload_project_image(
    file: UploadFile = File(...),
    storage: StorageService = Depends(
        get_storage_service
    ),
):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported image type.",
        )

    content = await file.read()

    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image exceeds the 10 MB limit.",
        )

    extension = (
        file.filename.rsplit(".", 1)[-1].lower()
        if file.filename and "." in file.filename
        else "jpg"
    )

    filename = f"{uuid4()}.{extension}"

    path = f"projects/{filename}"

    try:
        public_url = storage.upload(
            path,
            content,
            file.content_type,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Image upload failed.",
        ) from exc

    return {
        "filename": filename,
        "path": path,
        "url": public_url,
    }