import asyncio
import logging
from sqlalchemy import select

from collecte.core.database import get_db
from collecte.models.location import LocationModel
from collecte.schemas.location import LocationSchema
from collecte.services.groups import group_exists
from .utils import sqlalchemy_to_pydantic

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
        results = await session.execute(select(LocationModel.post_code).distinct())
        return results.scalars().all()


async def get_location(location: LocationSchema) -> LocationModel:
    """Return the id of the location object in the database"""
    location_db = LocationModel(**location.model_dump(exclude="collections"))
    async with get_db() as session:
        stmt = select(LocationModel).where(
            LocationModel.name == location.name,
            LocationModel.sampling_location_code == location.sampling_location_code,
            LocationModel.full_address == location.full_address,
            LocationModel.latitude == location.latitude,
            LocationModel.longitude == location.longitude,
        )
        result = await session.execute(stmt)
        existing_location = result.scalar_one_or_none()

        if existing_location:
            return existing_location
        
        # Ensure the group exists before creating the location
        if not await group_exists(gr_code=location.group_code):
            logger.warning(f"Group {location.group_code} does not exist for location: {location.city} {location.post_code}")
            return None
        
        # If location doesn't exist, create it
        session.add(location_db)
        await session.commit()
        await session.refresh(location_db)
        return location_db


async def save_locations(locations: list[LocationSchema]):
    """Retrieve all locations from API and store them in database"""
    tasks = [get_location(location) for location in locations]
    await asyncio.gather(*tasks)
