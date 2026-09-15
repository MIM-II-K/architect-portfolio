from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_project_service
from app.services.project_service import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get("")
async def list_projects(
    service: ProjectService = Depends(get_project_service),
):
    return await _list_projects(service)


@router.get("/{slug}")
async def get_project(
    slug: str,
    service: ProjectService = Depends(get_project_service),
):
    return await _get_project(slug, service)


async def _list_projects(service: ProjectService):
    return service.list_projects()


async def _get_project(
    slug: str,
    service: ProjectService,
):
    project = service.get_project(slug)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project