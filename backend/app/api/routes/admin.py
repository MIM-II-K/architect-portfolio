from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.api.dependencies import (
    get_category_service,
    get_project_service,
    get_inquiry_service,
)
from app.core.auth import require_admin
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.schemas.project import ProjectResponse
from app.schemas.project_admin import (
    ProjectCreate,
    ProjectUpdate,
)
from app.schemas.inquiry import (
    InquiryCreate,
    InquiryResponse,
    InquiryListResponse,
    InquiryStatusUpdate,
)
from app.schemas.admin_project import (
    AdminProjectListResponse,
    AdminProjectResponse,
    PublishProjectRequest,
    FeatureProjectRequest,
    ProjectOrderRequest,

)

from app.services.category_service import CategoryService
from app.services.project_service import ProjectService
from app.services.inquiry_service import InquiryService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)],
)


@router.get(
    "/projects",
    response_model=AdminProjectListResponse,
)
async def list_admin_projects(
    published: bool | None = None,
    featured: bool | None = None,
    q: str | None = None,
    service: ProjectService = Depends(get_project_service),
):
    projects = service.list_admin_projects(
        published=published,
        featured=featured,
        q=q,
    )

    return {
        "projects": projects,
        "total": len(projects),
    }


@router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    payload: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
):
    try:
        return service.create_project(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.patch(
    "/projects/{project_id}",
    response_model=ProjectResponse,
)
async def update_project(
    project_id: str,
    payload: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
):
    update_data = payload.model_dump(exclude_unset=True)

    try:
        project = service.update_project(
            project_id,
            update_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service),
):
    deleted = service.delete_project(project_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )


@router.get(
    "/inquiries",
    response_model=InquiryListResponse,
)
async def list_admin_inquiries(
    service: InquiryService = Depends(get_inquiry_service),
):
    inquiries = service.list_inquiries()
    return {
        "inquiries": inquiries,
        "total": len(inquiries),
    }

@router.patch(
    "/inquiries/{inquiry_id}/status",
    response_model=InquiryResponse,
)
async def update_inquiry_status(
    inquiry_id: str,
    payload: InquiryStatusUpdate,
    service: InquiryService = Depends(
        get_inquiry_service
    ),
):
    try:
        inquiry = service.update_status(
            inquiry_id,
            payload.status,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if inquiry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inquiry not found.",
        )

    return inquiry


@router.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    payload: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
):
    try:
        return service.create_category(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.patch(
    "/categories/{category_id}",
    response_model=CategoryResponse,
)
async def update_category(
    category_id: str,
    payload: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    try:
        category = service.update_category(
            category_id,
            payload.model_dump(exclude_unset=True),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return category


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    category_id: str,
    service: CategoryService = Depends(get_category_service),
):
    deleted = service.delete_category(category_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )


@router.patch(
    "/projects/{project_id}/publish",
    response_model=AdminProjectResponse,
)
async def set_project_published(
    project_id: str,
    payload: PublishProjectRequest,
    service: ProjectService = Depends(get_project_service),
):
    project = service.set_published(
        project_id,
        payload.published,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.patch(
    "/projects/{project_id}/featured",
    response_model=AdminProjectResponse,
)
async def set_project_featured(
    project_id: str,
    payload: FeatureProjectRequest,
    service: ProjectService = Depends(get_project_service),
):
    project = service.set_featured(
        project_id,
        payload.featured,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.patch(
    "/projects/{project_id}/order",
    response_model=AdminProjectResponse,
)
async def set_project_order(
    project_id: str,
    payload: ProjectOrderRequest,
    service: ProjectService = Depends(get_project_service),
):
    project = service.set_sort_order(
        project_id,
        payload.sort_order,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project