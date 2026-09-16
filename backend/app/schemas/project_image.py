from pydantic import BaseModel, Field


class ProjectImageCreate(BaseModel):
    image_url: str = Field(min_length=1)
    alt_text: str = Field(min_length=1, max_length=200)
    caption: str | None = None
    sort_order: int = Field(default=0, ge=0)


class ProjectImageUpdate(BaseModel):
    image_url: str | None = Field(
        default=None,
        min_length=1,
    )
    alt_text: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    caption: str | None = None
    sort_order: int | None = Field(
        default=None,
        ge=0,
    )


class ProjectImageResponse(ProjectImageCreate):
    id: str


class ProjectImageListResponse(BaseModel):
    images: list[ProjectImageResponse]
    total: int