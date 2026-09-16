from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from app.schemas.project_image import ProjectImageResponse
from app.schemas.pagination import PaginationMeta

class ProjectBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    location: str | None = None
    year: int | None = Field(default=None, ge=1900, le=2100)
    category: str | None = None
    area: str | None = None
    client: str | None = None
    architect: str | None = None
    status: str | None = None
    cover_image: str | None = None
    featured: bool = False
    published: bool = False
    sort_order: int = 0


class ProjectResponse(ProjectBase):
    id: str
    images: list[ProjectImageResponse] = Field(
        default_factory=list
    )
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ProjectListResponse(BaseModel):
    projects: list[ProjectResponse]
    pagination: PaginationMeta
    total: int