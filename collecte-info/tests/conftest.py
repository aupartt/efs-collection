import pytest
import json
from unittest.mock import AsyncMock
from pathlib import Path

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
)
from collecte.schemas import (
    GroupSchema,
    LocationSchema,
    CollectionSchema,
    CollectionGroupSchema,
    CollectionEventSchema,
    CollectionGroupSnapshotSchema,
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


# Fake schemas and models
def get_data_from_json(file_name: str) -> list[dict]:
    with open(TEST_DATA_DIR / file_name, "r") as f:
        return json.load(f)


@pytest.fixture
def mock_grp():
    groups = get_data_from_json("groups.json")

    class main:
        schemas: list[GroupSchema] = [GroupSchema(**group) for group in groups]
        models: list[GroupModel] = [GroupModel(**shema.model_dump()) for shema in schemas]
        api: list[SamplingGroupEntity] = [SamplingGroupEntity.from_dict(group) for group in groups]

    return main


@pytest.fixture
def mock_loc():
    locations = get_data_from_json("locations.json")

    class main:
        schemas: list[LocationSchema] = [LocationSchema(**location) for location in locations]
        models: list[LocationModel] = [LocationModel(**shema.model_dump()) for shema in schemas]
        api: list[SamplingLocationEntity] = [SamplingLocationEntity.from_dict(location) for location in locations]

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
