from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=1, max_length=100)
    description: str | None = None
    sort_order: int = 0
    active: bool = True


class CategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    description: str | None = None
    sort_order: int | None = None
    active: bool | None = None


class CategoryResponse(CategoryCreate):
    id: str


class CategoryListResponse(BaseModel):
    categories: list[CategoryResponse]
    total: int