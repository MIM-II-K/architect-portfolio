from datetime import datetime, timezone
from typing import Any

from google.cloud.firestore_v1 import Client


class CategoryRepository:
    COLLECTION_NAME = "categories"

    def __init__(self, db: Client):
        self.db = db

    def get_all(self) -> list[dict[str, Any]]:
        documents = (
            self.db
            .collection(self.COLLECTION_NAME)
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

    def get_by_slug(
        self,
        slug: str,
    ) -> dict[str, Any] | None:
        documents = (
            self.db
            .collection(self.COLLECTION_NAME)
            .where("slug", "==", slug)
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

    def get_by_id(
        self,
        category_id: str,
    ) -> dict[str, Any] | None:
        document = (
            self.db
            .collection(self.COLLECTION_NAME)
            .document(category_id)
            .get()
        )

        if not document.exists:
            return None

        return {
            "id": document.id,
            **document.to_dict(),
        }

    def create(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        now = datetime.now(timezone.utc)

        document_data = {
            **data,
            "created_at": now,
            "updated_at": now,
        }

        document_ref = (
            self.db
            .collection(self.COLLECTION_NAME)
            .document()
        )

        document_ref.set(document_data)

        return {
            "id": document_ref.id,
            **document_data,
        }

    def update(
        self,
        category_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any] | None:
        document_ref = (
            self.db
            .collection(self.COLLECTION_NAME)
            .document(category_id)
        )

        document = document_ref.get()

        if not document.exists:
            return None

        update_data = {
            **data,
            "updated_at": datetime.now(timezone.utc),
        }

        document_ref.update(update_data)

        updated_document = document_ref.get()

        return {
            "id": updated_document.id,
            **updated_document.to_dict(),
        }

    def delete(
        self,
        category_id: str,
    ) -> bool:
        document_ref = (
            self.db
            .collection(self.COLLECTION_NAME)
            .document(category_id)
        )

        document = document_ref.get()

        if not document.exists:
            return False

        document_ref.delete()

        return True