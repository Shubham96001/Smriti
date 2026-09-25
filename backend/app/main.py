"""
SmritiSaathi — Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.routes import auth, assessment


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for the FastAPI application."""
    # Note: In production, use Alembic for migrations instead of init_db()
    if settings.APP_ENV == "development":
        await init_db()
    yield
    await close_db()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    description="Backend API for SmritiSaathi web application",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api")
app.include_router(assessment.router, prefix="/api")

@app.get("/health", tags=["system"])
async def health_check():
    """System health check endpoint."""
    return {"status": "ok", "environment": settings.APP_ENV}
