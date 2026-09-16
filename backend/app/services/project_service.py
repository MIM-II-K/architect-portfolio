from typing import Any, Optional

from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(
        self,
        repository: ProjectRepository,
        image_repository: Any = None,
    ):
        self.repository = repository
        self.image_repository = image_repository

    def list_projects(self) -> list[dict[str, Any]]:
        projects = self.repository.get_all()

        published_projects = [
            project
            for project in projects
            if project.get("published") is True
        ]

        return [
            self._attach_images(project)
            for project in published_projects
        ]

    def list_featured_projects(self) -> list[dict[str, Any]]:
        projects = self.repository.get_all()

        featured = [
            project
            for project in projects
            if (
                project.get("published") is True
                and project.get("featured") is True
            )
        ]

        return [
            self._attach_images(project)
            for project in featured
        ]

    def get_project(
        self,
        slug: str,
    ) -> Optional[dict[str, Any]]:
        project = self.repository.get_by_slug(slug)

        if project is None:
            return None

        if project.get("published") is not True:
            return None

        return self._attach_images(project)

    def create_project(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        existing = self.repository.get_by_slug(data["slug"])

        if existing is not None:
            raise ValueError(
                "A project with this slug already exists."
            )

        project = self.repository.create(data)
        return self._attach_images(project)

    def update_project(
        self,
        project_id: str,
        data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        if "slug" in data:
            existing = self.repository.get_by_slug(data["slug"])

            if (
                existing is not None
                and existing["id"] != project_id
            ):
                raise ValueError(
                    "A project with this slug already exists."
                )

        updated_project = self.repository.update(
            project_id,
            data,
        )
        if updated_project is None:
            return None

        return self._attach_images(updated_project)

    def delete_project(
        self,
        project_id: str,
    ) -> bool:
        return self.repository.delete(project_id)

    def _attach_images(
        self,
        project: dict[str, Any],
    ) -> dict[str, Any]:
        if self.image_repository is None:
            project["images"] = []
            return project

        project["images"] = self.image_repository.get_all(
            project["id"]
        )

        return project