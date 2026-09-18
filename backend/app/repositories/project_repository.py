from datetime import datetime, timezone
from typing import Any, Optional
from supabase import Client


class ProjectRepository:
    TABLE_NAME = "projects"

    def __init__(self, client: Client):
        self.client = client

    def get_all(self) -> list[dict[str, Any]]:
        response = (
            self.client.table(self.TABLE_NAME)
            .select("*")
            .order("sort_order")
            .execute()
        )
        return response.data or []

    def get_by_id(self, project_id: str) -> Optional[dict[str, Any]]:
        response = (
            self.client.table(self.TABLE_NAME)
            .select("*")
            .eq("id", project_id)
            .execute()
        )
        return response.data[0] if response.data else None

    def get_by_slug(self, slug: str) -> Optional[dict[str, Any]]:
        response = (
            self.client.table(self.TABLE_NAME)
            .select("*")
            .eq("slug", slug)
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        payload = {
            **data,
            "created_at": now,
            "updated_at": now,
        }
        response = self.client.table(self.TABLE_NAME).insert(payload).execute()
        return response.data[0] if response.data else {}

    def update(self, project_id: str, data: dict[str, Any]) -> Optional[dict[str, Any]]:
        now = datetime.now(timezone.utc).isoformat()
        payload = {
            **data,
            "updated_at": now,
        }
        response = (
            self.client.table(self.TABLE_NAME)
            .update(payload)
            .eq("id", project_id)
            .execute()
        )
        return response.data[0] if response.data else None

    def delete(self, project_id: str) -> bool:
        response = (
            self.client.table(self.TABLE_NAME)
            .delete()
            .eq("id", project_id)
            .execute()
        )
        return bool(response.data)

    def get_admin_projects(self) -> list[dict[str, Any]]:
        return self.get_all()