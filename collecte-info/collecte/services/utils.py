import logging
from pydantic import BaseModel
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from api_carto_client import Client
from api_carto_client.models.ping import Ping
from api_carto_client.api.ping import get_carto_api_v3_ping as api_ping

from collecte.core.database import get_db
from collecte.models.base import BaseModel as SQLAlchemyBaseModel


logger = logging.getLogger(__name__)


def with_api_client(func):
    def wrapper(*args, **kwargs):
        client = Client(base_url="https://oudonner.api.efs.sante.fr/")
        with client as cli:
            return func(cli, *args, **kwargs)

    return wrapper

@with_api_client
def check_api(client: Client) -> bool:
    try:
        ping_resp: Ping = api_ping.sync(client=client)
        if ping_resp.version != "v3":
            logger.error(f"The server is running API in {ping_resp.version}, but only v3 is supported.")
            return False
        return True
    except Exception as e:
        logger.error(f"API check failed: {e}")
        return False

def api_to_pydantic(api_models: list, pydantic_model: BaseModel) -> list[BaseModel]:
    """Convert an API model to a Pydantic model"""
    return [pydantic_model(**api_model.to_dict()) for api_model in api_models]

def api_to_sqlalchemy(api_models: list, sqlalchemy_model: SQLAlchemyBaseModel) -> list[SQLAlchemyBaseModel]:
    """Convert an API model to a Pydantic model"""
    return [sqlalchemy_model(**api_model.to_dict()) for api_model in api_models]

def pydantic_to_sqlalchemy(pydantic_models: list[BaseModel], sqlalchemy_model: SQLAlchemyBaseModel) -> list[SQLAlchemyBaseModel]:
    """Convert a Pydantic model to an API model"""
    return [sqlalchemy_model(**pydantic_model.model_dump()) for pydantic_model in pydantic_models]

def sqlalchemy_to_pydantic(sqlalchemy_models: list[SQLAlchemyBaseModel], pydantic_model) -> list[BaseModel]:
    """Convert a SQLAlchemy model to a Pydantic model"""
    return [pydantic_model.model_validate(sqlalchemy_model) for sqlalchemy_model in sqlalchemy_models]

async def update_all(db_schema, items: list[BaseModel]):
    """Update/Create all items in database"""
    if isinstance(items[0], BaseModel):
        items = pydantic_to_sqlalchemy(items, db_schema)
    elif not isinstance(items[0], BaseModel):
        items = api_to_sqlalchemy(items, db_schema)

    async def _update_item(session: AsyncSession, item: SQLAlchemyBaseModel) -> None:
        try:
            db_item = await session.get(db_schema, item.gr_code)
            if not db_item:
                await session.add(item)
                logger.debug(f"Added {item.gr_code} to database")
            if db_item == item:
                return
            await db_item.update(item)
            logger.debug(f"Updated {item.gr_code} in database")
        except Exception as e:
            logger.error(f"Error updating {item.gr_code}: {e}")
            return
    
    async with get_db() as session:
        tasks = [_update_item(session, item) for item in items]
        await asyncio.gather(*tasks)
        await session.commit()
