from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.admin import router as admin_router
from app.api.routes.auth import router as auth_router
from app.api.routes.categories import router as categories_router
from app.api.routes.inquiries import router as inquiries_router
from app.api.routes.projects import router as projects_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.api.routes.project_images import (
    router as project_images_router,
)
from app.api.routes.uploads import (
    router as uploads_router,
)


settings = get_settings()

configure_logging()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "environment": settings.app_env,
    }


app.include_router(
    projects_router,
    prefix="/api",
)

app.include_router(
    categories_router,
    prefix="/api",
)

app.include_router(
    inquiries_router,
    prefix="/api",
)

app.include_router(
    auth_router,
    prefix="/api",
)

app.include_router(
    admin_router,
    prefix="/api",
)

app.include_router(
    project_images_router,
    prefix="/api",
)

app.include_router(
    uploads_router,
    prefix="/api",
)