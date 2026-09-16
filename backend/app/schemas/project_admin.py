from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
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


class ProjectUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        min_length=1,
    )

    location: str | None = None
    year: int | None = Field(default=None, ge=1900, le=2100)
    category: str | None = None
    area: str | None = None
    client: str | None = None
    architect: str | None = None
    status: str | None = None
    cover_image: str | None = None

    featured: bool | None = None
    published: bool | None = None
    sort_order: int | None = None