import asyncio
import contextlib

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from collecte.core.settings import settings

db_samaphore = asyncio.Semaphore(20)
engine = create_async_engine(
    settings.POSTGRES_URL.unicode_string(), pool_size=10, max_overflow=20
)
AsyncSessionLocal = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)


@contextlib.asynccontextmanager
async def get_db():
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
