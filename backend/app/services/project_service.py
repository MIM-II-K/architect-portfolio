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

    def list_admin_projects(
        self,
        published: bool | None = None,
        featured: bool | None = None,
        q: str | None = None,
    ) -> list[dict[str, Any]]:
        projects = self.repository.get_admin_projects()

        if published is not None:
            projects = [
                project 
                for project in projects
                if project.get("published") == published
            ]

        if featured is not None:
            projects = [
                project
                for project in projects
                if project.get("featured") == featured
            ]

        if q:
            query = q.lower().strip()

            projects = [
                project
                for project in projects
                if (
                    query in project.get("title", "").lower()
                    or query in project.get("description", "").lower()
                    or query in project.get("location", "").lower()
                )
            ]
        return [
            self._attach_images(project)
            for project in projects
        ]
    
    def set_published(
        self,
        project_id: str,
        published: bool,
    ) -> dict[str, Any] | None:
        return self.repository.update(
            project_id,
            {
                "published": published,
            },
        )

    def set_featured(
        self,
        project_id: str,
        featured: bool,
    ) -> dict[str, Any] | None:
        return self.repository.update(
            project_id,
            {
                "featured": featured,
            },
        )

    def set_sort_order(
        self,
        project_id: str,
        sort_order: int,
    ) -> dict[str, Any] | None:
        return self.repository.update(
            project_id,
            {
                "sort_order": sort_order,
            },
        )

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