from typing import Any

from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(
        self,
        repository: ProjectRepository,
    ):
        self.repository = repository

    def list_projects(self) -> list[dict[str, Any]]:
        return self.repository.get_all()

    def get_project(
        self,
        slug: str,
    ) -> dict[str, Any] | None:
        return self.repository.get_by_slug(slug)

    def create_project(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        existing = self.repository.get_by_slug(data["slug"])

        if existing is not None:
            raise ValueError(
                "A project with this slug already exists."
            )

        return self.repository.create(data)

    def update_project(
        self,
        project_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any] | None:
        if "slug" in data:
            existing = self.repository.get_by_slug(data["slug"])

            if (
                existing is not None
                and existing["id"] != project_id
            ):
                raise ValueError(
                    "A project with this slug already exists."
                )

        return self.repository.update(
            project_id,
            data,
        )

    def delete_project(
        self,
        project_id: str,
    ) -> bool:
        return self.repository.delete(project_id)