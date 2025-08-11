import logging

from collecte.schemas import ScheduleSchema, ScheduleGroupSchema, CollectionEventSchema
from collecte.services.schedules import retrieve_events, add_schedule
from collecte.services.collections import get_active_collections


logger = logging.getLogger(__name__)


async def _retrieve_active_collections_url() -> list[str]:
    """Retrieve all active collections from the database and return their URL"""
    active_collections = await get_active_collections()
    return [collection.url for collection in active_collections if collection]
