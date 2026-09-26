"""
SmritiSaathi — Database Connection

Async SQLAlchemy engine and session factory for PostgreSQL.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# Async engine for application use
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

# Session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


import app.models  # noqa: F401 - register every model with Base.metadata


async def get_db() -> AsyncSession:
    """
    Dependency that provides a database session.
    Automatically commits on success, rolls back on error.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create all tables (development only — use Alembic migrations in production)."""
    async with engine.begin() as conn:
        if conn.dialect.name == "postgresql":
            await conn.exec_driver_sql("CREATE SCHEMA IF NOT EXISTS public")
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Dispose engine connections on shutdown."""
    await engine.dispose()
