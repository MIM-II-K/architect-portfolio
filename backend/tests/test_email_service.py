# tests/test_email_service.py
from unittest.mock import patch

from app.services.email_service import EmailService


def test_inquiry_email_contains_details():
    service = EmailService()

    inquiry = {
        "name": "John",
        "email": "john@example.com",
        "phone": "+977 9800000000",
        "subject": "Residence",
        "message": "I want to discuss a residence.",
    }

    html = service._build_inquiry_html(inquiry)

    assert "John" in html
    assert "john@example.com" in html
    assert "Residence" in html
    assert "I want to discuss a residence." in html


def test_inquiry_email_escapes_html():
    service = EmailService()

    inquiry = {
        "name": "<script>alert(1)</script>",
        "email": "john@example.com",
        "subject": "Test",
        "message": "<b>hello</b>",
    }

    html = service._build_inquiry_html(inquiry)

    assert "<script>" not in html
    assert "&lt;script&gt;" in html
    assert "&lt;b&gt;hello&lt;/b&gt;" in html


@patch("app.services.email_service.resend.Emails.send")
def test_send_inquiry_notification(mock_send):
    service = EmailService()

    inquiry = {
        "name": "John",
        "email": "john@example.com",
        "phone": None,
        "subject": "Residence",
        "message": "I want to discuss a residence.",
    }

    service.send_inquiry_notification(inquiry)

    mock_send.assert_called_once()