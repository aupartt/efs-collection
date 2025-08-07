import logging
from sqlalchemy import select

from collecte.core.database import get_db
from collecte.schemas import CollectionDBSchema
from collecte.models import CollectionModel
from .utils import sqlalchemy_to_pydantic, update_all

logger = logging.getLogger(__name__)


async def load_collections() -> list[CollectionDBSchema]:
    async with get_db() as session:
        results = await session.execute(select(CollectionModel))
        collections = results.scalars().all()
        return sqlalchemy_to_pydantic(collections, CollectionDBSchema)


async def save_collections(collcetions: list[CollectionDBSchema]):
    await update_all(CollectionModel, collcetions)
