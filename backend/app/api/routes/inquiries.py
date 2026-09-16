import logging
from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_email_service, get_inquiry_service
from app.schemas.inquiry import InquiryCreate, InquiryResponse
from app.services.email_service import EmailService
from app.services.inquiry_service import InquiryService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/inquiries", tags=["Inquiries"])


@router.post("", response_model=InquiryResponse, status_code=status.HTTP_201_CREATED)
async def create_inquiry(
    payload: InquiryCreate,
    service: InquiryService = Depends(get_inquiry_service),
    email_service: EmailService = Depends(get_email_service),
):
    inquiry = service.create(payload.model_dump())

    try:
        email_service.send_inquiry_notification(inquiry)
    except Exception:
        logger.exception("Failed to send inquiry notification")

    return inquiry