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


async def api_to_pydantic(
    api_models: list, pydantic_model: BaseModel
) -> list[BaseModel]:
    """Convert an API model to a Pydantic model"""
    return [pydantic_model(**api_model.to_dict()) for api_model in api_models]


async def pydantic_to_sqlalchemy(
    pydantic_models: list[BaseModel], sqlalchemy_model: SQLAlchemyBaseModel
) -> list[SQLAlchemyBaseModel]:
    """Convert a Pydantic model to an API model"""
    return [
        sqlalchemy_model(**pydantic_model.model_dump())
        for pydantic_model in pydantic_models
    ]


async def sqlalchemy_to_pydantic(
    sqlalchemy_models: list[SQLAlchemyBaseModel], pydantic_model: BaseModel
) -> list[BaseModel]:
    """Convert a SQLAlchemy model to a Pydantic model"""
    return [
        pydantic_model(**sqlalchemy_model.__dict__)
        for sqlalchemy_model in sqlalchemy_models
    ]
