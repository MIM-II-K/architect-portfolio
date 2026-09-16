from typing import Any

from app.repositories.inquiry_repository import (
    InquiryRepository,
)


class InquiryService:
    ALLOWED_STATUSES = {
        "new",
        "read",
        "replied",
        "archived",
    }

    def __init__(
        self,
        repository: InquiryRepository,
    ):
        self.repository = repository

    def create(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        return self.repository.create(data)

    def list_inquiries(
        self,
    ) -> list[dict[str, Any]]:
        return self.repository.get_all()

    def update_status(
        self,
        inquiry_id: str,
        status: str,
    ) -> dict[str, Any] | None:
        if status not in self.ALLOWED_STATUSES:
            raise ValueError(
                f"Invalid inquiry status: {status}"
            )

        return self.repository.update_status(
            inquiry_id,
            status,
        )