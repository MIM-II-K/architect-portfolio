from typing import Any

from app.repositories.category_repository import (
    CategoryRepository,
)


class CategoryService:
    def __init__(
        self,
        repository: CategoryRepository,
    ):
        self.repository = repository

    def list_categories(self) -> list[dict[str, Any]]:
        return self.repository.get_all()

    def create_category(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        existing = self.repository.get_by_slug(
            data["slug"]
        )

        if existing is not None:
            raise ValueError(
                "A category with this slug already exists."
            )

        return self.repository.create(data)

    def update_category(
        self,
        category_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any] | None:
        if "slug" in data:
            existing = self.repository.get_by_slug(
                data["slug"]
            )

            if (
                existing is not None
                and existing["id"] != category_id
            ):
                raise ValueError(
                    "A category with this slug already exists."
                )

        return self.repository.update(
            category_id,
            data,
        )

    def delete_category(
        self,
        category_id: str,
    ) -> bool:
        return self.repository.delete(category_id)