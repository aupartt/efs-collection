import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from collecte.core.database import db_samaphore, get_db
from collecte.models import LocationModel
from collecte.schemas import LocationSchema
from collecte.services.groups import get_group

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


async def get_location(
    session: AsyncSession, location: LocationSchema
) -> LocationModel | None:
    """Return the id of the location object in the database"""
    stmt = select(LocationModel).where(
        LocationModel.name == location.name,
        LocationModel.sampling_location_code == location.sampling_location_code,
        LocationModel.full_address == location.full_address,
        LocationModel.latitude == location.latitude,
        LocationModel.longitude == location.longitude,
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def add_location(location: LocationSchema) -> LocationModel | None:
    """Add a location to database"""
    async with db_samaphore:
        async with get_db() as session:
            try:
                # Ensure the group exists before creating the location
                if not await get_group(session, gr_code=location.group_code):
                    logger.warning("No group found", extra={**location.info()})
                    return None

                location_db = await get_location(session, location)
                if not location_db:
                    location_db = LocationModel(**location.model_dump())
                    session.add(location_db)
                else:
                    for key, value in location.model_dump(
                        exclude={"id", "group_code", "collections"}
                    ).items():
                        setattr(location_db, key, value)

                await session.commit()
                await session.refresh(location_db)
                return location_db
            except Exception as e:
                logger.error(
                    "Failed to add/update location",
                    extra={**location.info(), "error": str(e)},
                )
                await session.rollback()


async def save_locations(locations: list[LocationSchema]) -> list[LocationModel | None]:
    """Retrieve all locations from API and store them in database"""
    tasks = [add_location(location) for location in locations]
    return await asyncio.gather(*tasks)
