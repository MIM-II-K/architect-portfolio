import pytest

from app.services.inquiry_service import InquiryService


class FakeInquiryRepository:
    def __init__(self):
        self.inquiries = []

    def create(self, data):
        inquiry = {
            "id": "inquiry-1",
            **data,
            "status": "new",
        }

        self.inquiries.append(inquiry)

        return inquiry

    def get_all(self):
        return self.inquiries

    def update_status(
        self,
        inquiry_id,
        status,
    ):
        for inquiry in self.inquiries:
            if inquiry["id"] == inquiry_id:
                inquiry["status"] = status
                return inquiry

        return None


def test_create_inquiry():
    repository = FakeInquiryRepository()
    service = InquiryService(repository)

    inquiry = service.create(
        {
            "name": "John",
            "email": "john@example.com",
            "subject": "Project",
            "message": "I want to discuss a project.",
        }
    )

    assert inquiry["status"] == "new"
    assert inquiry["email"] == "john@example.com"


def test_update_inquiry_status():
    repository = FakeInquiryRepository()
    service = InquiryService(repository)

    service.create(
        {
            "name": "John",
            "email": "john@example.com",
            "subject": "Project",
            "message": "I want to discuss a project.",
        }
    )

    inquiry = service.update_status(
        "inquiry-1",
        "read",
    )

    assert inquiry["status"] == "read"


def test_invalid_status():
    repository = FakeInquiryRepository()
    service = InquiryService(repository)

    with pytest.raises(ValueError):
        service.update_status(
            "inquiry-1",
            "banana",
        )