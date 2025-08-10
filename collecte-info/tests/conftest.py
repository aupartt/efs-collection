import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

from api_carto_client.models.sampling_group_entity import SamplingGroupEntity
from api_carto_client.models.sampling_location_entity import SamplingLocationEntity
from api_carto_client.models.sampling_location_collections_entity import (
    SamplingLocationCollectionsEntity,
)

from collecte.models import (
    GroupModel,
    LocationModel,
    CollectionGroupModel,
    CollectionEventModel,
    CollectionGroupSnapshotModel,
    ScheduleModel,
)
from collecte.schemas import (
    GroupSchema,
    LocationSchema,
    CollectionSchema,
    CollectionGroupSchema,
    CollectionEventSchema,
    CollectionGroupSnapshotSchema,
    ScheduleSchema,
    ScheduleGroupSchema,
    ScheduleEventSchema,
)


TEST_DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def async_cm():
    def _make(return_value):
        cm = AsyncMock()
        cm.__aenter__.return_value = return_value
        cm.__aexit__.return_value = None
        return cm

    return _make


@pytest.fixture
def mock_get_db(async_cm):
    def _make(value):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_results = MagicMock()
        mock_results.scalars.return_value.all.return_value = value
        mock_session.execute.return_value = mock_results
        return mock_session, async_cm(mock_session)

    return _make


# Fake schemas and models
def get_data_from_json(file_name: str) -> list[dict]:
    with open(TEST_DATA_DIR / file_name, "r") as f:
        return json.load(f)


@pytest.fixture
def mock_grp():
    groups = get_data_from_json("groups.json")

    class main:
        schemas: list[GroupSchema] = [GroupSchema(**group) for group in groups]
        models: list[GroupModel] = [
            GroupModel(**shema.model_dump()) for shema in schemas
        ]
        api: list[SamplingGroupEntity] = [
            SamplingGroupEntity.from_dict(group) for group in groups
        ]

    return main


@pytest.fixture
def mock_loc():
    locations = get_data_from_json("locations.json")

    class main:
        schemas: list[LocationSchema] = [
            LocationSchema(**location) for location in locations
        ]
        models: list[LocationModel] = [
            LocationModel(**shema.model_dump()) for shema in schemas
        ]
        api: list[SamplingLocationEntity] = [
            SamplingLocationEntity.from_dict(location) for location in locations
        ]

    return main


@pytest.fixture
def mock_loc_col():
    collections = get_data_from_json("collections.json")

    class main:
        schemas: list[LocationSchema] = [
            LocationSchema(**collection) for collection in collections
        ]
        api: list[SamplingLocationCollectionsEntity] = [
            SamplingLocationCollectionsEntity.from_dict(collection)
            for collection in collections
        ]

    return main


@pytest.fixture
def mock_col(mock_loc_col):
    class main:
        schemas: list[CollectionSchema] = mock_loc_col.schemas[0].collections

    return main


@pytest.fixture
def mock_grp_col(mock_col):
    class main:
        schemas: list[CollectionGroupSchema] = [
            schema.as_group(from_db=False) for schema in mock_col.schemas
        ]
        models: list[CollectionGroupModel] = [
            CollectionGroupModel(**shema.model_dump()) for shema in schemas
        ]

    return main


@pytest.fixture
def mock_evt_col(mock_grp_col):
    class main:
        schemas: list[CollectionEventSchema] = mock_grp_col.schemas[0].events
        models: list[CollectionEventModel] = [
            CollectionEventModel(**shema.model_dump()) for shema in schemas
        ]

    return main


@pytest.fixture
def mock_snap_col(mock_grp_col):
    class main:
        schemas: list[CollectionGroupSnapshotSchema] = mock_grp_col.schemas[0].snapshots
        models: list[CollectionGroupSnapshotModel] = [
            CollectionGroupSnapshotModel(**shema.model_dump()) for shema in schemas
        ]

    return main


@pytest.fixture
def mock_grp_sch():
    schedules = get_data_from_json("schedules.json")

    class main:
        schemas: list[ScheduleGroupSchema] = [
            ScheduleGroupSchema(**schedule) for schedule in schedules
        ]

    return main


@pytest.fixture
def mock_evt_sch(mock_grp_sch):
    class main:
        schemas: list[ScheduleEventSchema] = mock_grp_sch.schemas[0].events

    return main


@pytest.fixture
def mock_sch(mock_grp_sch):
    class main:
        schemas: list[ScheduleSchema] = [
            schema for schema in mock_grp_sch.schemas[0].build()
        ]
        models: list[ScheduleModel] = [
            ScheduleModel(**schema.model_dump()) for schema in schemas
        ]

    return main
