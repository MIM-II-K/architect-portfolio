import resend

from app.core.config import settings


def initialize_email() -> None:
    resend.api_key = settings.RESEND_API_KEY