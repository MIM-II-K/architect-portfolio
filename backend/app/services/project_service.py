from typing import Any, Optional

from app.repositories.project_image_repository import ProjectImageRepository
from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(
        self,
        repository: ProjectRepository,
        image_repository: Optional[ProjectImageRepository] = None,
    ):
        self.repository = repository
        self.image_repository = image_repository

    def list_projects(
        self,
        category: str | None = None,
        year: int | None = None,
        location: str | None = None,
        sort: str = "order",
    ) -> list[dict[str, Any]]:
        projects = self.repository.get_all()

        # Filter published projects
        projects = [
            project for project in projects if project.get("published") is True
        ]

        if category:
            category_query = category.strip().lower()
            projects = [
                project
                for project in projects
                if project.get("category", "").lower() == category_query
            ]

        if year is not None:
            projects = [
                project for project in projects if project.get("year") == year
            ]

        if location:
            location_query = location.strip().lower()
            projects = [
                project
                for project in projects
                if location_query in project.get("location", "").lower()
            ]

        # Sorting logic
        if sort == "newest":
            projects.sort(
                key=lambda p: p.get("year") or 0,
                reverse=True,
            )
        elif sort == "oldest":
            projects.sort(
                key=lambda p: p.get("year") or 0,
            )
        elif sort == "title_asc":
            projects.sort(
                key=lambda p: p.get("title", "").lower(),
            )
        elif sort == "title_desc":
            projects.sort(
                key=lambda p: p.get("title", "").lower(),
                reverse=True,
            )
        else:
            projects.sort(
                key=lambda p: p.get("sort_order", 0),
            )

        return [self._attach_images(project) for project in projects]

    def list_admin_projects(
        self,
        published: bool | None = None,
        featured: bool | None = None,
        q: str | None = None,
    ) -> list[dict[str, Any]]:
        projects = self.repository.get_admin_projects()

        if published is not None:
            projects = [
                p for p in projects if p.get("published") == published
            ]

        if featured is not None:
            projects = [
                p for p in projects if p.get("featured") == featured
            ]

        if q:
            query = q.lower().strip()
            projects = [
                p
                for p in projects
                if (
                    query in p.get("title", "").lower()
                    or query in p.get("description", "").lower()
                    or query in p.get("location", "").lower()
                )
            ]

        return [self._attach_images(project) for project in projects]

    def set_published(
        self,
        project_id: str,
        published: bool,
    ) -> dict[str, Any] | None:
        updated = self.repository.update(project_id, {"published": published})
        return self._attach_images(updated) if updated else None

    def set_featured(
        self,
        project_id: str,
        featured: bool,
    ) -> dict[str, Any] | None:
        updated = self.repository.update(project_id, {"featured": featured})
        return self._attach_images(updated) if updated else None

    def set_sort_order(
        self,
        project_id: str,
        sort_order: int,
    ) -> dict[str, Any] | None:
        updated = self.repository.update(project_id, {"sort_order": sort_order})
        return self._attach_images(updated) if updated else None

    def list_featured_projects(self) -> list[dict[str, Any]]:
        projects = self.repository.get_all()

        featured = [
            p
            for p in projects
            if p.get("published") is True and p.get("featured") is True
        ]

        return [self._attach_images(project) for project in featured]

    def get_project(
        self,
        slug: str,
    ) -> Optional[dict[str, Any]]:
        project = self.repository.get_by_slug(slug)

        if project is None or project.get("published") is not True:
            return None

        return self._attach_images(project)

    def create_project(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        existing = self.repository.get_by_slug(data["slug"])

        if existing is not None:
            raise ValueError("A project with this slug already exists.")

        project = self.repository.create(data)

        # Sync cover_image into the image subcollection if provided
        cover_image = project.get("cover_image")
        if cover_image and self.image_repository:
            self.image_repository.create(
                project["id"],
                {
                    "project_id": project["id"],
                    "image_url": cover_image,
                    "alt_text": project.get("title") or "Cover Image",
                    "caption": project.get("title"),
                    "sort_order": 0,
                },
            )

        return self._attach_images(project)

    def update_project(
        self,
        project_id: str,
        data: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        if "slug" in data:
            existing = self.repository.get_by_slug(data["slug"])

            if existing is not None and existing["id"] != project_id:
                raise ValueError("A project with this slug already exists.")

        updated_project = self.repository.update(project_id, data)
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
        images = []
        if self.image_repository is not None:
            raw_images = self.image_repository.get_all(project["id"])
            for img in raw_images:
                images.append({
                    "id": img.get("id", ""),
                    "image_url": img.get("image_url") or img.get("url", ""),
                    "alt_text": img.get("alt_text") or project.get("title") or "Image",
                    "caption": img.get("caption"),
                    "sort_order": img.get("sort_order", 0),
                })

        # Fallback: If subcollection is empty but cover_image exists
        cover_image = project.get("cover_image")
        if not images and cover_image:
            images = [
                {
                    "id": "cover",
                    "image_url": cover_image,
                    "alt_text": project.get("title") or "Cover Image",
                    "caption": None,
                    "sort_order": 0,
                }
            ]

        project["images"] = images
        return project