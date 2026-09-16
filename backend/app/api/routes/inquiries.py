from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_inquiry_service
from app.schemas.inquiry import (
    InquiryCreate,
    InquiryResponse,
)
from app.services.inquiry_service import InquiryService


router = APIRouter(
    prefix="/inquiries",
    tags=["Inquiries"],
)


@router.post(
    "",
    response_model=InquiryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_inquiry(
    payload: InquiryCreate,
    service: InquiryService = Depends(
        get_inquiry_service
    ),
):
    return service.create(
        payload.model_dump()
    )