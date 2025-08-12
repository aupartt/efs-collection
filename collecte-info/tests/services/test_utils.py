import pytest
from api_carto_client.models.ping import Ping
from pydantic import BaseModel as PydanticBaseModel

import collecte.services.utils as utils_services
from collecte.models import GroupModel
from collecte.models.base import Base as SQLAlchemyBaseModel
from collecte.schemas import GroupSchema


@pytest.mark.asyncio
async def test_check_api_success(mocker):
    mock_ping = Ping(version="v3")
    mock_api_ping = mocker.patch(
        "collecte.services.utils.api_ping.asyncio", return_value=mock_ping
    )

    result = await utils_services.check_api()

    mock_api_ping.assert_awaited()
    assert result is True


@pytest.mark.asyncio
async def test_check_api_wrong_version(mocker):
    mock_ping = Ping(version="v2")
    mock_api_ping = mocker.patch(
        "collecte.services.utils.api_ping.asyncio", return_value=mock_ping
    )
    mock_log = mocker.patch.object(utils_services.logger, "error")

    result = await utils_services.check_api()

    mock_api_ping.assert_awaited()
    mock_log.assert_called_once()
    assert result is False


@pytest.mark.asyncio
async def test_check_api_exception(mocker):
    mock_api_ping = mocker.patch(
        "collecte.services.utils.api_ping.asyncio",
        side_effect=Exception("Connection error"),
    )
    mock_log = mocker.patch.object(utils_services.logger, "error")

    result = await utils_services.check_api()

    mock_api_ping.assert_awaited()
    mock_log.assert_called_once()
    assert result is False


@pytest.mark.asyncio
async def test_api_to_pydantic(mock_grp):
    api_schemas = mock_grp.api

    result = await utils_services.api_to_pydantic(api_schemas, GroupSchema)

    assert result == mock_grp.schemas


@pytest.mark.asyncio
async def test_pydantic_to_sqlalchemy(mock_grp):
    pydantic_schemas = mock_grp.schemas

    result = await utils_services.pydantic_to_sqlalchemy(pydantic_schemas, GroupModel)

    assert [all(isinstance(grp, GroupModel) for grp in result)]
    assert len(result) == len(pydantic_schemas)


@pytest.mark.asyncio
async def test_sqlalchemy_to_pydantic(mock_grp):
    sqlalchemy_models = mock_grp.models

    result = await utils_services.sqlalchemy_to_pydantic(sqlalchemy_models, GroupSchema)

    assert result == mock_grp.schemas


@pytest.mark.asyncio
async def test_api_to_pydantic_empty_list():
    api_models = []

    result = await utils_services.api_to_pydantic(api_models, PydanticBaseModel)

    assert result == []


@pytest.mark.asyncio
async def test_pydantic_to_sqlalchemy_empty_list():
    pydantic_models = []

    result = await utils_services.pydantic_to_sqlalchemy(
        pydantic_models, SQLAlchemyBaseModel
    )

    assert result == []


@pytest.mark.asyncio
async def test_sqlalchemy_to_pydantic_empty_list():
    sqlalchemy_models = []

    result = await utils_services.sqlalchemy_to_pydantic(
        sqlalchemy_models, PydanticBaseModel
    )

    assert result == []
