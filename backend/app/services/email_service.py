from html import escape
from typing import Any

import resend

from app.core.config import settings

class EmailService:
    def send_inquiry_notification(self, inquiry: dict[str, Any]) -> None:
        resend.Emails.send(
            {
                "from": settings.RESEND_FROM_EMAIL,
                "to": settings.INQUIRY_NOTIFICATION_EMAIL,
                "subject": f"New Inquiry from {escape(inquiry['subject'])}",
                "html": self._build_inquiry_html(inquiry),
            }
        )
    
    def _build_inquiry_html(self, inquiry: dict[str, Any]) -> str:
        name =  escape(str(inquiry.get("name", "")))
        email = escape(str(inquiry.get("email", "")))
        phone = escape(str(inquiry.get("phone", "")))  
        subject = escape(str(inquiry.get("subject", "")))
        message = escape(str(inquiry.get("message", "")))

        return f"""
        <h2>New Portfolio Inquiry</h2>

        <p>
            <strong>Name:</strong> {name}
        </p>

        <p>
            <strong>Email:</strong> {email}
        </p>

        <p>
            <strong>Phone:</strong> {phone}
        </p>

        <p>
            <strong>Subject:</strong> {subject}
        </p>

        <hr>

        <p>
            <strong>Message:</strong>
        </p>

        <p>{message}</p>
        """