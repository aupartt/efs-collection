import logging

from sqlalchemy import select

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


async def save_groups(groups: list[GroupSchema]) -> None:
    """Retrieve groups from API and add them to database"""

    await update_all(groups, GroupModel)
