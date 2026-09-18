import logging
from supabase import Client
from app.core.config import settings

logger = logging.getLogger(__name__)


class StorageService:
    def __init__(self, client: Client):
        self.client = client
        self.bucket = settings.SUPABASE_STORAGE_BUCKET  

    def upload(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str,
        folder: str = "",
    ) -> dict[str, str]:
        """Uploads file bytes to Supabase storage and returns public URL and storage path."""
        from uuid import uuid4
        
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "jpg"
        unique_filename = f"{uuid4()}.{ext}"
        
        # Build clean storage path
        clean_folder = folder.strip("/")
        clean_path = f"{clean_folder}/{unique_filename}" if clean_folder else unique_filename

        try:
            logger.info(f"Uploading file to bucket '{self.bucket}' at path '{clean_path}'...")

            # 1. Perform Upload
            self.client.storage.from_(self.bucket).upload(
                path=clean_path,
                file=file_bytes,
                file_options={
                    "content-type": content_type,
                    "upsert": "true",
                },
            )

            # 2. Get Public URL
            res_url = self.client.storage.from_(self.bucket).get_public_url(clean_path)

            if isinstance(res_url, str):
                public_url = res_url
            elif isinstance(res_url, dict):
                public_url = res_url.get("publicUrl") or res_url.get("public_url", "")
            else:
                public_url = getattr(res_url, "public_url", getattr(res_url, "publicUrl", str(res_url)))

            logger.info(f"Successfully uploaded: {public_url}")
            
            return {
                "public_url": public_url,
                "path": clean_path,
            }

        except Exception as exc:
            logger.error(f"Failed to upload {clean_path} to bucket '{self.bucket}': {exc}")
            raise exc

    def delete(self, path: str) -> None:
        """Removes a file from the Supabase storage bucket."""
        clean_path = path.lstrip("/")
        try:
            self.client.storage.from_(self.bucket).remove([clean_path])
            logger.info(f"Successfully deleted {clean_path} from bucket '{self.bucket}'")
        except Exception as exc:
            logger.error(
                f"Failed to delete {clean_path} from bucket '{self.bucket}': {exc}"
            )
            raise exc