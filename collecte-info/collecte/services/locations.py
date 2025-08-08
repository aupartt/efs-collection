import logging
from sqlalchemy import select

from collecte.core.database import get_db
from collecte.models import LocationModel
from collecte.schemas import LocationSchema
from .utils import sqlalchemy_to_pydantic, update_all

logger = logging.getLogger(__name__)


async def load_locations() -> list[LocationSchema]:
    """Return all location from database"""
    async with get_db() as session:
        results = await session.execute(select(LocationModel))
        locations = results.scalars().all()
        return await sqlalchemy_to_pydantic(locations, LocationSchema)

async def get_postal_codes() -> list[str]:
    """Return all unique postal code from database"""
    async with get_db() as session:
        results = await session.execute(select(LocationModel.postal_code).distinct())
        return results.scalars().all()

async def save_locations(locations: list[LocationSchema]):
    """Retrieve all locations from API and store them in database"""
    await update_all(locations, LocationModel)
