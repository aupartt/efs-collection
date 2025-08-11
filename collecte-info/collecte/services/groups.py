import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from collecte.core.database import get_db, db_samaphore
from collecte.models import GroupModel
from collecte.schemas import GroupSchema

from .utils import sqlalchemy_to_pydantic

logger = logging.getLogger(__name__)


async def load_groups() -> list[GroupSchema]:
    """Return all groups from database"""
    async with get_db() as session:
        stmt = select(GroupModel)
        results = await session.execute(stmt)
        groups = results.scalars().all()

        return await sqlalchemy_to_pydantic(groups, GroupSchema)


async def get_group(session: AsyncSession, gr_code: str) -> GroupModel | None:
    """Return a group from database"""
    stmt = select(GroupModel).filter_by(gr_code=gr_code)
    results = await session.execute(stmt)
    return results.scalar_one_or_none()


async def add_group(group: GroupSchema) -> GroupModel | None:
    """Add a group to database"""
    async with db_samaphore:
        async with get_db() as session:
            try:
                stmt = select(GroupModel).where(GroupModel.gr_code == group.gr_code)
                result = await session.execute(stmt)
                existing_group = result.scalar_one_or_none()

                if existing_group:
                    for key, value in group.model_dump(
                        exclude={"gr_code", "locations"}
                    ).items():
                        setattr(existing_group, key, value)
                else:
                    existing_group = GroupModel(**group.model_dump())
                    session.add(existing_group)

                await session.commit()
                await session.refresh(existing_group)
                return existing_group
            except Exception as e:
                logger.error(f"Error adding group {group.gr_code}: {e}")
                await session.rollback()


async def save_groups(groups: list[GroupSchema]) -> None:
    """ADD/UPDATE all groups to database"""
    tasks = [add_group(group) for group in groups]
    await asyncio.gather(*tasks)
