from app.integrations.firebase import get_firestore_client
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService


def get_project_service() -> ProjectService:
    db = get_firestore_client()

    repository = ProjectRepository(db)

    return ProjectService(repository)