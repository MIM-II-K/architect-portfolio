from app.services.project_service import ProjectService


class FakeProjectRepository:
    def __init__(self, projects):
        self.projects = projects

    def get_all(self):
        return self.projects

    def get_by_slug(self, slug):
        for project in self.projects:
            if project["slug"] == slug:
                return project

        return None


class FakeImageRepository:
    def get_all(self, project_id):
        return [
            {
                "id": "image-1",
                "image_url": "https://example.com/test.jpg",
                "alt_text": "Test image",
                "caption": None,
                "sort_order": 1,
            }
        ]


def test_only_published_projects_are_public():
    repository = FakeProjectRepository(
        [
            {
                "id": "1",
                "slug": "published",
                "published": True,
                "featured": False,
            },
            {
                "id": "2",
                "slug": "draft",
                "published": False,
                "featured": False,
            },
        ]
    )

    service = ProjectService(
        repository,
        FakeImageRepository(),
    )

    projects = service.list_projects()

    assert len(projects) == 1
    assert projects[0]["slug"] == "published"


def test_draft_is_not_public():
    repository = FakeProjectRepository(
        [
            {
                "id": "1",
                "slug": "draft",
                "published": False,
                "featured": False,
            }
        ]
    )

    service = ProjectService(
        repository,
        FakeImageRepository(),
    )

    project = service.get_project("draft")

    assert project is None


def test_featured_requires_published():
    repository = FakeProjectRepository(
        [
            {
                "id": "1",
                "slug": "featured-public",
                "published": True,
                "featured": True,
            },
            {
                "id": "2",
                "slug": "featured-draft",
                "published": False,
                "featured": True,
            },
        ]
    )

    service = ProjectService(
        repository,
        FakeImageRepository(),
    )

    projects = service.list_featured_projects()

    assert len(projects) == 1
    assert projects[0]["slug"] == "featured-public"