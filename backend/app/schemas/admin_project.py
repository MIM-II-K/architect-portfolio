from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.project_image import ProjectImageResponse


class AdminProjectResponse(BaseModel):
    id: str
    title: str
    slug: str
    description: str

    location: str | None = None
    year: int | None = None
    category: str | None = None
    area: str | None = None
    client: str | None = None
    architect: str | None = None
    status: str | None = None
    cover_image: str | None = None

    featured: bool = False
    published: bool = False
    sort_order: int = 0

    images: list[ProjectImageResponse] = Field(
        default_factory=list
    )

    created_at: datetime | None = None
    updated_at: datetime | None = None


class AdminProjectListResponse(BaseModel):
    projects: list[AdminProjectResponse]
    total: int


class PublishProjectRequest(BaseModel):
    published: bool


class FeatureProjectRequest(BaseModel):
    featured: bool


class ProjectOrderRequest(BaseModel):
    sort_order: int