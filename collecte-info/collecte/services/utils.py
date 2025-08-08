import logging
from pydantic import BaseModel
import asyncio

from sqlalchemy.inspection import inspect

from api_carto_client import Client
from api_carto_client.models.ping import Ping
from api_carto_client.api.ping import get_carto_api_v3_ping as api_ping

from collecte.core.database import get_db
from collecte.models.base import BaseModel as SQLAlchemyBaseModel


logger = logging.getLogger(__name__)


def with_api_client(func):
    async def wrapper(*args, **kwargs):
        client = Client(base_url="https://oudonner.api.efs.sante.fr/")
        async with client as cli:
            return await func(cli, *args, **kwargs)

    return wrapper


@with_api_client
async def check_api(client: Client) -> bool:
    try:
        ping_resp: Ping = await api_ping.asyncio(client=client)
        if ping_resp.version != "v3":
            logger.error(
                f"The server is running API in {ping_resp.version}, but only v3 is supported."
            )
            return False
        return True
    except Exception as e:
        logger.error(f"API check failed: {e}")
        return False


def api_to_pydantic(api_models: list, pydantic_model: BaseModel) -> list[BaseModel]:
    """Convert an API model to a Pydantic model"""
    return [pydantic_model(**api_model.to_dict()) for api_model in api_models]


def api_to_sqlalchemy(
    api_models: list, sqlalchemy_model: SQLAlchemyBaseModel
) -> list[SQLAlchemyBaseModel]:
    """Convert an API model to a Pydantic model"""
    return [sqlalchemy_model(**api_model.to_dict()) for api_model in api_models]


def pydantic_to_sqlalchemy(
    pydantic_models: list[BaseModel], sqlalchemy_model: SQLAlchemyBaseModel
) -> list[SQLAlchemyBaseModel]:
    """Convert a Pydantic model to an API model"""
    return [
        sqlalchemy_model(**pydantic_model.model_dump())
        for pydantic_model in pydantic_models
    ]


def sqlalchemy_to_pydantic(
    sqlalchemy_models: list[SQLAlchemyBaseModel], pydantic_model: BaseModel
) -> list[BaseModel]:
    """Convert a SQLAlchemy model to a Pydantic model"""
    return [
        pydantic_model(**sqlalchemy_model.__dict__)
        for sqlalchemy_model in sqlalchemy_models
    ]


async def update_all(items: list, db_schema: SQLAlchemyBaseModel):
    """Update or create all items in the database asynchronously.

    Args:
        items: A list of items to update or create in the database.
        db_schema: The SQLAlchemy model class representing the table schema.
    """
    if not items:
        return

    # Convert items to SQLAlchemy models if necessary
    if isinstance(items[0], BaseModel):
        items = pydantic_to_sqlalchemy(items, db_schema)
    elif not isinstance(items[0], SQLAlchemyBaseModel):
        items = api_to_sqlalchemy(items, db_schema)

    async def _update_item(item: SQLAlchemyBaseModel) -> None:
        async with get_db() as session:
            try:
                # Get the primary key from the model class
                primary_key = inspect(item.__class__).primary_key
                if not primary_key:
                    logger.error("No primary key found for the item.")
                    return

                # Assuming single primary key for simplicity
                pk_name = primary_key[0].name
                pk_value = getattr(item, pk_name, None)
                
                db_item = await session.get(db_schema, pk_value)

                # Add new item
                if not db_item:
                    session.add(item)
                    await session.commit()
                    logger.debug(f"Added a new object in table {item.__tablename__}")
                    return

                # Item exists, and hasn't changed
                if db_item == item:
                    return

                # Item exists, update it
                for key, value in item.__dict__.items():
                    setattr(db_item, key, value)
                await session.commit()
                logger.debug(
                    f"Updated object {pk_value} in table {item.__tablename__}"
                )
            except Exception as e:
                await session.rollback()  # Rollback in case of error
                logger.error(
                    f"Error updating {pk_value} in table {item.__tablename__}: {e}"
                )
            

    tasks = [_update_item(item) for item in items]
    await asyncio.gather(*tasks)
