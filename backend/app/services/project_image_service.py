from typing import Any

from app.repositories.project_image_repository import (
    ProjectImageRepository,
)
from app.repositories.project_repository import (
    ProjectRepository,
)


class ProjectImageService:
    def __init__(
        self,
        image_repository: ProjectImageRepository,
        project_repository: ProjectRepository,
    ):
        self.image_repository = image_repository
        self.project_repository = project_repository

    def list_images(
        self,
        project_id: str,
    ) -> list[dict[str, Any]]:
        project = self.project_repository.get_by_id(
            project_id
        )

        if project is None:
            raise LookupError("Project not found.")

        return self.image_repository.get_all(project_id)

    def create_image(
        self,
        project_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        project = self.project_repository.get_by_id(
            project_id
        )

        if project is None:
            raise LookupError("Project not found.")

        return self.image_repository.create(
            project_id,
            data,
        )

    def delete_image(
        self,
        project_id: str,
        image_id: str,
    ) -> bool:
        return self.image_repository.delete(
            project_id,
            image_id,
        )