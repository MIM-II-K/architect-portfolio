from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


class InquiryRepository:
    COLLECTION_NAME = "inquiries"

    def __init__(self, db):
        self.db = db

    def create(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        inquiry_id = str(uuid4())

        document = {
            **data,
            "status": "new",
            "created_at": datetime.now(
                timezone.utc
            ),
        }

        self.db.collection(
            self.COLLECTION_NAME
        ).document(inquiry_id).set(document)

        return {
            "id": inquiry_id,
            **document,
        }

    def get_all(self) -> list[dict[str, Any]]:
        documents = (
            self.db
            .collection(self.COLLECTION_NAME)
            .order_by(
                "created_at",
                direction="DESCENDING",
            )
            .stream()
        )

        return [
            {
                "id": document.id,
                **document.to_dict(),
            }
            for document in documents
        ]

    def get_by_id(
        self,
        inquiry_id: str,
    ) -> dict[str, Any] | None:
        document = (
            self.db
            .collection(self.COLLECTION_NAME)
            .document(inquiry_id)
            .get()
        )

        if not document.exists:
            return None

        return {
            "id": document.id,
            **document.to_dict(),
        }

    def update_status(
        self,
        inquiry_id: str,
        status: str,
    ) -> dict[str, Any] | None:
        reference = (
            self.db
            .collection(self.COLLECTION_NAME)
            .document(inquiry_id)
        )

        document = reference.get()

        if not document.exists:
            return None

        reference.update({
            "status": status,
        })

        return self.get_by_id(inquiry_id)