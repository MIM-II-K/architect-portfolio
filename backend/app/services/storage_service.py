from pathlib import Path

from supabase import Client

from app.core.config import settings


class StorageService:
    def __init__(self, client: Client):
        self.client = client
        self.bucket = settings.supabase_storage_bucket
    def upload(
        self,
        path: str,
        content: bytes,
        content_type: str,
    ) -> str:
        self.client.storage.from_(
            self.bucket
        ).upload(
            path,
            content,
            {
                "content-type": content_type,
                "upsert": "false",
            },
        )

        return (
            self.client.storage
            .from_(self.bucket)
            .get_public_url(path)
        )

    def delete(self, path: str) -> None:
        self.client.storage.from_(
            self.bucket
        ).remove([path])