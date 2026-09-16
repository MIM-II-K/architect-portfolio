from datetime import datetime, timezone
from typing import Any

from google.cloud.firestore_v1 import Client


class ProjectImageRepository:
    def __init__(self, db: Client):
        self.db = db

    def _collection(self, project_id: str):
        return (
            self.db
            .collection("projects")
            .document(project_id)
            .collection("images")
        )

    def get_all(
        self,
        project_id: str,
    ) -> list[dict[str, Any]]:
        documents = (
            self._collection(project_id)
            .order_by("sort_order")
            .stream()
        )

        return [
            {
                "id": document.id,
                **document.to_dict(),
            }
            for document in documents
        ]

    def create(
        self,
        project_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        now = datetime.now(timezone.utc)

        document_data = {
            **data,
            "created_at": now,
            "updated_at": now,
        }

        document_ref = self._collection(
            project_id
        ).document()

        document_ref.set(document_data)

        return {
            "id": document_ref.id,
            **document_data,
        }

    def delete(
        self,
        project_id: str,
        image_id: str,
    ) -> bool:
        document_ref = (
            self._collection(project_id)
            .document(image_id)
        )

        document = document_ref.get()

        if not document.exists:
            return False

        document_ref.delete()

        return True