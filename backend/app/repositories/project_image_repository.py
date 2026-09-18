from datetime import datetime, timezone
from typing import Any, Optional
from supabase import Client


class ProjectImageRepository:
    TABLE_NAME = "project_images"

    def __init__(self, client: Client):
        self.client = client

    def get_all(self, project_id: str) -> list[dict[str, Any]]:
        response = (
            self.client.table(self.TABLE_NAME)
            .select("*")
            .eq("project_id", project_id)
            .order("sort_order")
            .execute()
        )
        return response.data or []

    def get_by_id(self, project_id: str, image_id: str) -> Optional[dict[str, Any]]:
        response = (
            self.client.table(self.TABLE_NAME)
            .select("*")
            .eq("id", image_id)
            .eq("project_id", project_id)
            .execute()
        )
        return response.data[0] if response.data else None

    def create(self, project_id: str, data: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        payload = {
            **data,
            "project_id": project_id,
            "created_at": now,
            "updated_at": now,
        }
        response = self.client.table(self.TABLE_NAME).insert(payload).execute()
        return response.data[0] if response.data else {}

    def delete(self, project_id: str, image_id: str) -> bool:
        response = (
            self.client.table(self.TABLE_NAME)
            .delete()
            .eq("id", image_id)
            .eq("project_id", project_id)
            .execute()
        )
        return bool(response.data)