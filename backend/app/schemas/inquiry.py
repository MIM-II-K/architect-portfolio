from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class InquiryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str | None = Field(
        default=None,
        max_length=30,
    )
    subject: str = Field(min_length=3, max_length=200)
    message: str = Field(min_length=10, max_length=5000)


class InquiryResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str | None = None
    subject: str
    message: str
    status: str
    created_at: datetime | None = None


class InquiryListResponse(BaseModel):
    inquiries: list[InquiryResponse]
    total: int


class InquiryStatusUpdate(BaseModel):
    status: str