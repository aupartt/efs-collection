import logging

from sqlalchemy import select

from collecte.core.database import get_db
from collecte.models import ScheduleModel
from collecte.schemas import ScheduleSchema, CollectionEventSchema

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


async def retrieve_events(
    schedule: ScheduleSchema,
) -> list[CollectionEventSchema] | None:
    async with get_db() as session:
        """Check if the schedule is linked to a collection.
        Retrieve all events of that collection and return the ones that occure at the the same date
        """
        try:
            collection_db = await get_collection(session, schedule.efs_id)

            if not collection_db:
                logger.warning(f"Collection not found for schedule {schedule.info()}")
                return None

            await collection_db.awaitable_attrs.events
            return [
                CollectionEventSchema.model_validate(event)
                for event in collection_db.events
                if event.date == schedule.date
            ]
        except Exception as e:
            logger.error(
                f"Error while retrieving events for schedule {schedule.info()}: {e}"
            )

async def add_schedule(schedule: ScheduleSchema) -> ScheduleModel | None:
    """Save a single schedule"""
    async with get_db() as session:
        try:
            schedule_db = ScheduleModel(**schedule.model_dump())
            session.add(schedule_db)
            await session.commit()
            await session.refresh(schedule_db)
            return schedule_db
        except Exception as e:
            logger.error(f"Error while saving schedule {schedule.info()}: {e}")
