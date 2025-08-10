import pytest
import json
from unittest.mock import AsyncMock
from pathlib import Path

from collecte.models.group import GroupModel
from collecte.schemas.group import GroupSchema

from collecte.models.location import LocationModel
from collecte.schemas.location import LocationSchema

from collecte.models.collection import (
    CollectionGroupModel,
    CollectionEventModel,
    CollectionGroupSnapshotModel,
)
from collecte.schemas.collection import (
    CollectionSchema,
    CollectionGroupSchema,
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
        schemas = [GroupSchema(**group) for group in groups]
        models = [GroupModel(**shema.model_dump()) for shema in schemas]

    return main


@pytest.fixture
def mock_loc():
    locations = get_data_from_json("locations.json")

    class main:
        schemas = [LocationSchema(**location) for location in locations]
        models = [LocationModel(**shema.model_dump()) for shema in schemas]

    return main


@pytest.fixture
def mock_loc_col():
    collections = get_data_from_json("collections.json")

    class main:
        schemas = [LocationSchema(**collection) for collection in collections]

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
        models = [CollectionGroupModel(**shema.model_dump()) for shema in schemas]

    return main


@pytest.fixture
def mock_evt_col(mock_grp_col):
    class main:
        schemas = mock_grp_col.schemas[0].events
        models = [CollectionEventModel(**shema.model_dump()) for shema in schemas]

    return main


@pytest.fixture
def mock_snap_col(mock_grp_col):
    class main:
        schemas = mock_grp_col.schemas[0].snapshots
        models = [
            CollectionGroupSnapshotModel(**shema.model_dump()) for shema in schemas
        ]

    return main
