from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.api.dependencies import get_project_service
from app.schemas.project import (
    ProjectListResponse,
    ProjectResponse,
)
from app.schemas.project_admin import (
    ProjectCreate,
    ProjectUpdate,
)
from app.services.project_service import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get(
    "",
    response_model=ProjectListResponse,
)
async def list_projects(
    service: ProjectService = Depends(
        get_project_service
    ),
):
    projects = service.list_projects()

    return {
        "projects": projects,
        "total": len(projects),
    }


@router.get(
    "/{slug}",
    response_model=ProjectResponse,
)
async def get_project(
    slug: str,
    service: ProjectService = Depends(
        get_project_service
    ),
):
    project = service.get_project(slug)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    payload: ProjectCreate,
    service: ProjectService = Depends(
        get_project_service
    ),
):
    try:
        return service.create_project(
            payload.model_dump()
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def update_project(
    project_id: str,
    payload: ProjectUpdate,
    service: ProjectService = Depends(
        get_project_service
    ),
):
    update_data = payload.model_dump(
        exclude_unset=True
    )

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
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: str,
    service: ProjectService = Depends(
        get_project_service
    ),
):
    deleted = service.delete_project(project_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )