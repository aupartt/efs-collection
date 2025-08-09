import logging

from sqlalchemy import exists, select

from collecte.services.utils import update_all
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

async def save_groups(groups: list[GroupSchema]) -> None:
    """Retrieve groups from API and add them to database"""

    await update_all(groups, GroupModel)
