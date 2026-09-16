from app.services.project_service import ProjectService


class FakeProjectRepository:
    def __init__(self, projects):
        self.projects = projects

    def get_all(self):
        return self.projects

    def get_admin_projects(self):
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


def test_admin_can_see_drafts():
    repository = FakeProjectRepository(
        [
            {
                "id": "1",
                "slug": "published",
                "title": "Published Project",
                "description": "Public project",
                "location": "Palpa",
                "published": True,
                "featured": False,
            },
            {
                "id": "2",
                "slug": "draft",
                "title": "Draft Project",
                "description": "Private project",
                "location": "Palpa",
                "published": False,
                "featured": False,
            },
        ]
    )

    service = ProjectService(
        repository,
        FakeImageRepository(),
    )

    projects = service.list_admin_projects()

    assert len(projects) == 2


def test_admin_can_filter_drafts():
    repository = FakeProjectRepository(
        [
            {
                "id": "1",
                "slug": "published",
                "title": "Published Project",
                "description": "Public project",
                "location": "Palpa",
                "published": True,
                "featured": False,
            },
            {
                "id": "2",
                "slug": "draft",
                "title": "Draft Project",
                "description": "Private project",
                "location": "Palpa",
                "published": False,
                "featured": False,
            },
        ]
    )

    service = ProjectService(
        repository,
        FakeImageRepository(),
    )

    projects = service.list_admin_projects(
        published=False
    )

    assert len(projects) == 1
    assert projects[0]["slug"] == "draft"


def test_admin_project_search():
    repository = FakeProjectRepository(
        [
            {
                "id": "1",
                "slug": "mountain-residence",
                "title": "Mountain Residence",
                "description": "A residence in the hills",
                "location": "Palpa",
                "published": True,
                "featured": False,
            },
            {
                "id": "2",
                "slug": "city-office",
                "title": "City Office",
                "description": "Commercial office",
                "location": "Kathmandu",
                "published": True,
                "featured": False,
            },
        ]
    )

    service = ProjectService(
        repository,
        FakeImageRepository(),
    )

    projects = service.list_admin_projects(
        q="mountain"
    )

    assert len(projects) == 1
    assert projects[0]["slug"] == "mountain-residence"


def test_filter_projects_by_category():
    repository = FakeProjectRepository(
        [
            {
                "id": "1",
                "slug": "house",
                "title": "Mountain House",
                "description": "House",
                "location": "Palpa",
                "category": "Residential",
                "year": 2026,
                "published": True,
                "featured": False,
                "sort_order": 1,
            },
            {
                "id": "2",
                "slug": "office",
                "title": "City Office",
                "description": "Office",
                "location": "Kathmandu",
                "category": "Commercial",
                "year": 2026,
                "published": True,
                "featured": False,
                "sort_order": 2,
            },
        ]
    )

    service = ProjectService(
        repository,
        FakeImageRepository(),
    )

    projects = service.list_projects(
        category="residential"
    )

    assert len(projects) == 1
    assert projects[0]["slug"] == "house"

def test_filter_projects_by_year():
    repository = FakeProjectRepository(
        [
            {
                "id": "1",
                "slug": "project-2026",
                "title": "Project 2026",
                "description": "Project",
                "location": "Palpa",
                "category": "Residential",
                "year": 2026,
                "published": True,
                "featured": False,
                "sort_order": 1,
            },
            {
                "id": "2",
                "slug": "project-2025",
                "title": "Project 2025",
                "description": "Project",
                "location": "Palpa",
                "category": "Residential",
                "year": 2025,
                "published": True,
                "featured": False,
                "sort_order": 2,
            },
        ]
    )

    service = ProjectService(
        repository,
        FakeImageRepository(),
    )

    projects = service.list_projects(
        year=2026
    )

    assert len(projects) == 1
    assert projects[0]["year"] == 2026

def test_combined_project_filters():
    repository = FakeProjectRepository(
        [
            {
                "id": "1",
                "slug": "matching",
                "title": "Mountain House",
                "description": "House",
                "location": "Palpa",
                "category": "Residential",
                "year": 2026,
                "published": True,
                "featured": False,
                "sort_order": 1,
            },
            {
                "id": "2",
                "slug": "wrong-year",
                "title": "Another House",
                "description": "House",
                "location": "Palpa",
                "category": "Residential",
                "year": 2025,
                "published": True,
                "featured": False,
                "sort_order": 2,
            },
            {
                "id": "3",
                "slug": "wrong-category",
                "title": "Palpa Office",
                "description": "Office",
                "location": "Palpa",
                "category": "Commercial",
                "year": 2026,
                "published": True,
                "featured": False,
                "sort_order": 3,
            },
        ]
    )

    service = ProjectService(
        repository,
        FakeImageRepository(),
    )

    projects = service.list_projects(
        category="Residential",
        year=2026,
        location="Palpa",
    )

    assert len(projects) == 1
    assert projects[0]["slug"] == "matching"

def test_sort_projects_newest():
    repository = FakeProjectRepository(
        [
            {
                "id": "1",
                "slug": "older",
                "title": "Older",
                "description": "",
                "year": 2023,
                "published": True,
                "featured": False,
                "sort_order": 1,
            },
            {
                "id": "2",
                "slug": "newer",
                "title": "Newer",
                "description": "",
                "year": 2026,
                "published": True,
                "featured": False,
                "sort_order": 2,
            },
        ]
    )

    service = ProjectService(
        repository,
        FakeImageRepository(),
    )

    projects = service.list_projects(
        sort="newest"
    )

    assert projects[0]["slug"] == "newer"
    assert projects[1]["slug"] == "older"

def test_filters_never_expose_unpublished_projects():
    repository = FakeProjectRepository(
        [
            {
                "id": "1",
                "slug": "draft",
                "title": "Draft",
                "description": "",
                "category": "Residential",
                "year": 2026,
                "published": False,
                "featured": True,
            }
        ]
    )

    service = ProjectService(
        repository,
        FakeImageRepository(),
    )

    projects = service.list_projects(
        category="Residential",
        year=2026,
    )

    assert projects == []