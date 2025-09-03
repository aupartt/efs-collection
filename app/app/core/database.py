from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

engine = create_engine(settings.POSTGRES_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """Dependency to get database session"""
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()
