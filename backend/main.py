from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.routes import router as auth_router
from ai.routes import router as ai_router
from assessments.routes import router as assessments_router
from caregivers.routes import router as caregivers_router
from config import settings
from database import check_connection, close_pool, open_pool
from games.routes import router as games_router
from memory.routes import router as memory_router
from reminders.routes import router as reminders_router
from sync.routes import router as sync_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    open_pool()
    yield
    close_pool()


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(auth_router, prefix="/api")
app.include_router(assessments_router, prefix="/api")
app.include_router(games_router, prefix="/api")
app.include_router(ai_router, prefix="/api")
app.include_router(memory_router, prefix="/api")
app.include_router(reminders_router, prefix="/api")
app.include_router(caregivers_router, prefix="/api")
app.include_router(sync_router, prefix="/api")


@app.get("/api/health", tags=["system"])
def health() -> dict[str, str]:
    database_status = "up" if check_connection() else "down"
    return {"status": "ok" if database_status == "up" else "degraded", "api": "up", "database": database_status}


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"name": settings.app_name, "docs": "/docs"}