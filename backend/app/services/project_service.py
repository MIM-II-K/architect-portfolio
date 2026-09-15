from typing import Any

from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def list_projects(self) -> list[dict[str, Any]]:
        return self.repository.get_all()

    def get_project(self, slug: str) -> dict[str, Any] | None:
        return self.repository.get_by_slug(slug)