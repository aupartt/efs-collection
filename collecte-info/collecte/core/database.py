import contextlib

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from collecte.core.settings import settings


engine = create_async_engine(settings.POSTGRES_URL.unicode_string())
AsyncSessionLocal = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)


@contextlib.asynccontextmanager
async def get_db():
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
