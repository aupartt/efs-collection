import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from collecte.core.database import get_db, db_samaphore
from collecte.models import ScheduleModel
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