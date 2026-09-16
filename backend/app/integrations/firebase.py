from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore

from app.core.config import get_settings

settings = get_settings()


def initialize_firebase():
    if firebase_admin._apps:
        return firebase_admin.get_app()

    # Priority 1: Use raw credentials from environment variables (Deployment / CI)
    if settings.firebase_client_email and settings.firebase_private_key:
        private_key = settings.firebase_private_key.replace("\\n", "\n")
        cred = credentials.Certificate(
            {
                "type": "service_account",
                "project_id": settings.firebase_project_id,
                "client_email": settings.firebase_client_email,
                "private_key": private_key,
            }
        )
    # Priority 2: Fall back to firebase-key.json file (Local Development)
    else:
        # Resolve path relative to backend root folder
        backend_dir = Path(__file__).resolve().parent.parent.parent
        cred_path = backend_dir / settings.firebase_credentials_path

        if not cred_path.exists():
            raise FileNotFoundError(
                f"Firebase credentials not found at {cred_path}. "
                "Provide env vars or place firebase-key.json in backend/"
            )

        cred = credentials.Certificate(str(cred_path))

    return firebase_admin.initialize_app(
        cred,
        {
            "projectId": settings.firebase_project_id,
        },
    )


def get_firestore_client():
    initialize_firebase()
    return firestore.client()