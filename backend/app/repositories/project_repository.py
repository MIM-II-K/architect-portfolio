from typing import Any

from google.cloud.firestore_v1 import Client


class ProjectRepository:
    COLLECTION_NAME = "projects"

    def __init__(self, db: Client):
        self.db = db

    def get_all(self) -> list[dict[str, Any]]:
        documents = (
            self.db
            .collection(self.COLLECTION_NAME)
            .order_by("sort_order")
            .stream()
        )

        projects = []

        for document in documents:
            data = document.to_dict()

            projects.append(
                {
                    "id": document.id,
                    **data,
                }
            )

        return projects

    def get_by_slug(self, slug: str) -> dict[str, Any] | None:
        documents = (
            self.db
            .collection(self.COLLECTION_NAME)
            .where(
                "slug",
                "==",
                slug,
            )
            .limit(1)
            .stream()
        )

        document = next(documents, None)

        if document is None:
            return None

        return {
            "id": document.id,
            **document.to_dict(),
        }