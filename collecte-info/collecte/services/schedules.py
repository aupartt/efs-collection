import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from collecte.core.database import get_db, db_samaphore
from collecte.models import (ScheduleModel, CollectionEventModel)
from collecte.schemas import ScheduleSchema

from collecte.services.utils import sqlalchemy_to_pydantic
from collecte.services.collections import get_collection


logger = logging.getLogger(__name__)


async def load_schedules() -> list[ScheduleSchema]:
    """Return all groups from database"""
    async with get_db() as session:
        try:
            stmt = select(ScheduleModel)
            results = await session.execute(stmt)
            schdules = results.scalars().all()
            return await sqlalchemy_to_pydantic(schdules, ScheduleSchema)
        except Exception as e:
            logger.error(f"Error while loading schedules: {e}")


async def _retrieve_events(schedule: ScheduleSchema) -> list[CollectionEventModel] | None:
    async with get_db() as session:
        try:
            collection_db = await get_collection(session, schedule.efs_id)

            if not collection_db:
                logger.warning(f"Collection not found for schedule {schedule.info()}")
                return None
            
            await collection_db.awaitable_attrs.events
            return collection_db.events
        except Exception as e:
            logger.error(f"Error while retrieving events for schedule {schedule.info()}: {e}")
