import asyncio
import logging

from sqlalchemy import exists, select

from collecte.core.database import get_db
from collecte.models.group import GroupModel
from collecte.schemas.group import GroupSchema

from .utils import sqlalchemy_to_pydantic

logger = logging.getLogger(__name__)


async def load_groups() -> list[GroupSchema]:
    """Return all groups from database"""
    async with get_db() as session:
        results = await session.execute(select(GroupModel))
        groups = results.scalars().all()

        return await sqlalchemy_to_pydantic(groups, GroupSchema)


async def group_exists(gr_code: str) -> GroupSchema | None:
    """Return a group from database by gr_code, gr_lib or gr_desd"""
    async with get_db() as session:
        stmt = select(exists().where(GroupModel.gr_code == gr_code))
        results = await session.execute(stmt)
        return results.scalars()


async def add_group(group: GroupSchema) -> GroupModel:
    """Add a group to database"""
    async with get_db() as session:
        try:
            stmt = select(GroupModel).where(GroupModel.gr_code == group.gr_code)
            result = await session.execute(stmt)
            existing_group = result.scalar_one_or_none()
            if existing_group:
                for key, value in group.model_dump().items():
                    setattr(existing_group, key, value)
            else:
                session.add(GroupModel(**group.model_dump()))
        
            await session.commit()
        except Exception as e:
            logger.error(f"Error adding group {group.gr_code}: {e}")
            await session.rollback()

async def save_groups(groups: list[GroupSchema]) -> None:
    """ADD/UPDATE all groups to database"""
    tasks = [add_group(group) for group in groups]
    await asyncio.gather(*tasks)
