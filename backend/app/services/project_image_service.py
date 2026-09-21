from typing import Any
from fastapi import UploadFile

from app.repositories.project_image_repository import ProjectImageRepository
from app.repositories.project_repository import ProjectRepository
from app.services.storage_service import StorageService


class ProjectImageService:
    def __init__(
        self,
        image_repository: ProjectImageRepository,
        project_repository: ProjectRepository,
        storage_service: StorageService | None = None,
    ):
        self.image_repository = image_repository
        self.project_repository = project_repository
        self.storage_service = storage_service

    def list_images(self, project_id: str) -> dict[str, Any]:
        project = self.project_repository.get_by_id(project_id)
        if project is None:
            raise LookupError("Project not found.")

        raw_images = self.image_repository.get_all(project_id)
        formatted_images = [
            {
                "id": img.get("id", ""),
                "image_url": img.get("image_url") or img.get("url", ""),
                "alt_text": img.get("alt_text") or project.get("title") or "Image",
                "caption": img.get("caption"),
                "sort_order": img.get("sort_order", 0),
            }
            for img in raw_images
        ]

        return {
            "images": formatted_images,
            "total": len(formatted_images),
        }

    async def upload_image(
        self,
        project_id: str,
        file: UploadFile,
        alt_text: str | None = None,
        caption: str | None = None,
    ) -> dict[str, Any]:
        project = self.project_repository.get_by_id(project_id)
        if project is None:
            raise LookupError("Project not found.")

        if not self.storage_service:
            raise RuntimeError("Storage service is not configured.")

        # Read contents asynchronously to ensure complete file bytes are buffered
        file_bytes = await file.read()

        if not file_bytes:
            raise ValueError("Uploaded file is empty.")

        storage_info = self.storage_service.upload(
            file_bytes=file_bytes,
            filename=file.filename or "uploaded_image.jpg",
            content_type=file.content_type or "image/jpeg",
            folder=f"projects/{project_id}",
        )

        image_data = {
            "project_id": project_id,
            "image_url": storage_info["public_url"],
            "storage_path": storage_info["path"],
            "alt_text": alt_text or project.get("title") or "Image",
            "caption": caption,
            "sort_order": 0,
        }

        created = self.image_repository.create(project_id, image_data)

        return {
            "id": created.get("id", ""),
            "image_url": created.get("image_url"),
            "alt_text": created.get("alt_text") or project.get("title") or "Image",
            "caption": created.get("caption"),
            "sort_order": created.get("sort_order", 0),
        }

    def delete_image(self, project_id: str, image_id: str) -> bool:
        image_data = self.image_repository.get_by_id(project_id, image_id)
        if not image_data:
            return False

        storage_path = image_data.get("storage_path") or image_data.get("path")
        if self.storage_service and storage_path:
            try:
                self.storage_service.delete(storage_path)
            except Exception:
                pass

        return self.image_repository.delete(project_id, image_id)