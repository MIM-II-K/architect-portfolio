import pytest
from pydantic import ValidationError

from app.schemas.project import ProjectBase


def test_project_requires_title():
    with pytest.raises(ValidationError):
        ProjectBase(
            title="",
            slug="test-project",
            description="Test description",
        )


def test_project_rejects_invalid_year():
    with pytest.raises(ValidationError):
        ProjectBase(
            title="Test Project",
            slug="test-project",
            description="Test description",
            year=1800,
        )


def test_project_accepts_valid_data():
    project = ProjectBase(
        title="Test Project",
        slug="test-project",
        description="Test description",
        year=2026,
    )

    assert project.title == "Test Project"
    assert project.year == 2026