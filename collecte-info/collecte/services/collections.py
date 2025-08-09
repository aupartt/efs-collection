import logging
from sqlalchemy import select

from collecte.core.database import get_db
from collecte.schemas.collection import CollectionGroupSchema
from collecte.models.collection import (
    CollectionGroupModel,
)
from collecte.models.location import LocationModel
from collecte.services.groups import group_exists
from .utils import sqlalchemy_to_pydantic

logger = logging.getLogger(__name__)


async def load_collection_groups() -> list[CollectionGroupSchema]:
    async with get_db() as session:
        results = await session.execute(select(CollectionGroupModel))
        collections = results.scalars().all()
        return sqlalchemy_to_pydantic(collections, CollectionGroupSchema)


async def save_collection_group(
    collection_group_data: CollectionGroupSchema, location: LocationModel
) -> None:
    async with get_db() as session:
        results = await session.execute(
            select(CollectionGroupModel).filter_by(efs_id=collection_group_data.efs_id)
        )
        collection_group = results.scalars().first()

        # Check if group exists in database
        if not await group_exists(collection_group_data.gr_code):
            logger.warning(
                f"Group {collection_group_data.gr_code} not found in database for the location: {location.city} {location.post_code}"
            )
            return

        # CollectionGroup doesn't exist, create it
        if not collection_group:
            collection_group_db = CollectionGroupModel(
                **collection_group_data.model_dump(), location=location
            )

            session.add(collection_group_db)
            await session.commit()
            await session.refresh(collection_group_db)
            return collection_group_db

        session.merge(collection_group)

        await session.commit()
        await session.refresh(collection_group_db)
        return collection_group_db
