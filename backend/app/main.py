from dotenv import load_dotenv

# Load environment variables from .env before anything else reads them
load_dotenv()

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes.admin import router as admin_router
from app.api.routes.auth import router as auth_router
from app.api.routes.categories import router as categories_router
from app.api.routes.inquiries import router as inquiries_router
from app.api.routes.project_images import router as project_images_router
from app.api.routes.projects import router as projects_router
from app.api.routes.uploads import router as uploads_router

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.integrations.email import initialize_email


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_email()
    yield


settings = get_settings()

configure_logging()

app = FastAPI(
    title=settings.app_name,
    description="Backend API for an architect portfolio and content management system.",
    version="1.0.0",
    lifespan=lifespan,
)

# Ensure local upload directory exists and serve it statically
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Define allowed origins
origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin for origin in origins if origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "ok",
        "environment": settings.app_env,
    }


app.include_router(projects_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(inquiries_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(project_images_router, prefix="/api")
app.include_router(uploads_router, prefix="/api")