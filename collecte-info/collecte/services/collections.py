import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from collecte.core.database import get_db, db_samaphore

# Schemas
from collecte.schemas import (
    CollectionGroupSchema,
    CollectionEventSchema,
    CollectionGroupSnapshotSchema,
)
from collecte.schemas.location import LocationSchema

# Models
from collecte.models import (
    CollectionGroupModel,
    CollectionEventModel,
    CollectionGroupSnapshotModel,
)

# Services
from collecte.services.locations import get_location

from .utils import sqlalchemy_to_pydantic

logger = logging.getLogger(__name__)


async def load_collection_groups() -> list[CollectionGroupSchema]:
    async with get_db() as session:
        results = await session.execute(select(CollectionGroupModel))
        collections = results.scalars().all()
        return await sqlalchemy_to_pydantic(collections, CollectionGroupSchema)


async def get_collection(
    session: AsyncSession, efs_id: str
) -> CollectionGroupModel | None:
    stmt = select(CollectionGroupModel).filter_by(
        efs_id=efs_id
    )
    results = await session.execute(stmt)
    return results.scalar_one_or_none()


async def get_event(
    session: AsyncSession, event_id: int
) -> CollectionEventModel | None:
    stmt = select(CollectionEventModel).filter_by(id=event_id)
    results = await session.execute(stmt)
    return results.scalar_one_or_none()


async def _handle_location(location: LocationSchema) -> list[CollectionGroupSchema]:
    async with db_samaphore:
        async with get_db() as session:
            try:
                location_db = await get_location(session, location)
                if not location_db:
                    logger.warning(f"Location {location.info()} not found")
                    return

                collections = []
                for collection in location.collections:
                    collection.location_id = location_db.id
                    collections.append(collection)

                return collections
            except Exception as e:
                logger.error(f"Error while handling location {location.info()} : {e}")
                return []


async def _handle_collection(
    collection: CollectionGroupSchema,
) -> tuple[list[CollectionGroupSnapshotSchema], list[CollectionEventSchema]] | None:
    async with db_samaphore:
        async with get_db() as session:
            try:
                # Don't handle collection without efs_id
                # This is usually because the collection is not already available
                if not collection.efs_id:
                    logger.warning(
                        f"Couldn't get efs_id for collection {collection.info()}"
                    )
                    return

                collection_db = await get_collection(session, collection)

                if not collection_db:
                    # Collection does not exist, create it
                    collection_db = CollectionGroupModel(**collection.model_dump())
                    session.add(collection_db)
                    await session.commit()
                    return
                else:
                    # Collection does exist, update the values
                    for key, value in collection.model_dump(
                        exclude={"id","location_id", "events", "snapshots"}
                    ).items():
                        setattr(collection_db, key, value)

                await session.commit()
                await session.refresh(collection_db)

                # Update the ids of the events and snapshots
                collection.update_ids(collection_db.id)

                return collection.events, collection.snapshots
            except Exception as e:
                logger.error(f"Error while handling collection {collection.info()} : {e}")


async def _handle_event(event: CollectionEventSchema) -> CollectionEventModel:
    async with db_samaphore:
        async with get_db() as session:
            try:
                event_db = await get_event(session, event.id)

                # Collection does not exist, create it
                if not event_db:
                    event_db = CollectionEventModel(**event.model_dump())
                    session.add(event_db)
                else:
                    # Collection does exist, update the values
                    for key, value in event.model_dump().items():
                        setattr(event_db, key, value)

                await session.commit()
                await session.refresh(event_db)
                return event_db
            except Exception as e:
                logger.error(f"Error while handling event {event.id} : {e}")


async def _handle_snapshot(
    snapshot: CollectionGroupSnapshotSchema,
) -> CollectionGroupSnapshotModel:
    async with db_samaphore:
        async with get_db() as session:
            db_snapshot = CollectionGroupSnapshotModel(**snapshot.model_dump())
            session.add(db_snapshot)
            await session.commit()
            await session.refresh(db_snapshot)
            return db_snapshot


async def save_location_collections(
    locations: list[LocationSchema],
) -> tuple[int, int, int]:
    # Add a good docstring for this function
    """Save the collections of a list of locations in the database."""

    # Add location.id to each collection
    tasks = [_handle_location(location) for location in locations]
    collections_groups = await asyncio.gather(*tasks)

    # Check and update collections groups
    tasks = [
        _handle_collection(collection)
        for collections in collections_groups
        if collections
        for collection in collections
    ]
    items_groups = await asyncio.gather(*tasks)

    # Check and update events
    events = [event for items in items_groups if items for event in items[0]]
    tasks = [_handle_event(event) for event in events]

    await asyncio.gather(*tasks)

    # Add all snapshots
    snapshots = [snapshot for items in items_groups if items for snapshot in items[1]]
    tasks = [_handle_snapshot(snapshot) for snapshot in snapshots]
    await asyncio.gather(*tasks)

    return len(items_groups), len(events), len(snapshots)
