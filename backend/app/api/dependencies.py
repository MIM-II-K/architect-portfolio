from app.integrations.firebase import get_firestore_client
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService

from app.repositories.category_repository import (
    CategoryRepository,
)
from app.services.category_service import CategoryService

from app.repositories.project_image_repository import (
    ProjectImageRepository,
)
from app.services.project_image_service import (
    ProjectImageService,
)


def get_project_service() -> ProjectService:
    db = get_firestore_client()

    repository = ProjectRepository(db)

    return ProjectService(repository)

def get_category_service() -> CategoryService:
    db = get_firestore_client()

    repository = CategoryRepository(db)

    return CategoryService(repository)

def get_project_image_service() -> ProjectImageService:
    db = get_firestore_client()

    image_repository = ProjectImageRepository(db)
    project_repository = ProjectRepository(db)

    return ProjectImageService(
        image_repository,
        project_repository,
    )