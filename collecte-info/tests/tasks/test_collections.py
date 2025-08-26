import pytest
from aioresponses import aioresponses
from api_carto_client.models.sampling_collection_result import SamplingCollectionResult
from pytest_mock import MockerFixture

import collecte.tasks.collections as tasks_collections
from collecte.schemas import CollectionGroupSchema


class TestRetrieveSamplingCollections:
    @pytest.mark.asyncio
    async def test_success(self, mocker, mock_loc_col):
        mock_result = SamplingCollectionResult(
            sampling_location_collections=mock_loc_col.api
        )

        mock_api_search_collection = mocker.patch(
            "collecte.tasks.collections.api_search_collection.asyncio",
            return_value=mock_result,
        )

        result = await tasks_collections._retrieve_sampling_collections("35000")

        mock_api_search_collection.assert_awaited_with(
            client=mocker.ANY,
            post_code="35000",
            # hide_private_collects=True,
            # hide_non_publiable_collects=True,
            limit=100,
            user_latitude=48,
            user_longitude=-2,
            max_date=mocker.ANY,
        )
        assert result == mock_loc_col.api

    @pytest.mark.asyncio
    async def test_empty(self, mocker):
        mock_api_search_collection = mocker.patch(
            "collecte.tasks.collections.api_search_collection.asyncio",
            return_value=None,
        )

        result = await tasks_collections._retrieve_sampling_collections("35000")

        mock_api_search_collection.assert_awaited()
        assert result == []


class TestGetEsfId:
    @pytest.fixture
    def aiores(self):
        with aioresponses() as m:
            yield m

    def _mock_url(self, efs_id="123456"):
        return f"https://example.com/trouver-une-collecte/{efs_id}/"

    @pytest.mark.asyncio
    async def test_success(self, aiores):
        efs_id = "138799"
        url = self._mock_url(efs_id)
        aiores.head(url)
        result = await tasks_collections.get_efs_id(url)

        assert result == efs_id

    @pytest.mark.asyncio
    async def test_no_match(self, aiores):
        url = "http://example.com/path/to/page"
        aiores.head(url)
        result = await tasks_collections.get_efs_id(url)

        assert result is None

    @pytest.mark.asyncio
    async def test_empty_url(self):
        result = await tasks_collections.get_efs_id("")
        assert result is None

        result = await tasks_collections.get_efs_id(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_exception(self, mocker, aiores):
        url = self._mock_url()
        aiores.head(url, exception=Exception)

        mock_log = mocker.patch.object(tasks_collections.logger, "error")

        result = await tasks_collections.get_efs_id(url)

        mock_log.assert_called_once()
        assert result is None


class TestGetCollectionsLocations:
    @pytest.mark.asyncio
    async def test_success(self, mocker, mock_loc, mock_loc_col):
        mocker.patch("collecte.tasks.collections.check_api", return_value=True)
        mock_get_postal_codes = mocker.patch(
            "collecte.tasks.collections.get_postal_codes",
            return_value=["35000", "42000"],
        )

        mock__locations = [mock_loc_col.api[:2], mock_loc_col.api[2:]]
        mock_retrieve_sampling_collections = mocker.patch(
            "collecte.tasks.collections._retrieve_sampling_collections",
            side_effect=mock__locations,
        )

        result = await tasks_collections._get_collections_locations()

        mock_get_postal_codes.assert_awaited()
        mock_retrieve_sampling_collections.asser_awaited()
        assert len(result) == len(mock_loc_col.api)
        assert all(isinstance(loc, dict) for loc in result)

    @pytest.mark.asyncio
    async def test_api_check_fails(self, mocker):
        mock_check_api = mocker.patch(
            "collecte.tasks.collections.check_api", return_value=False
        )

        result = await tasks_collections._get_collections_locations()

        mock_check_api.assert_awaited()
        assert result == []


class TestHandleLocation:
    @pytest.mark.asyncio
    async def test_success(self, mocker, mock_loc_col):
        loc_col = mock_loc_col.schemas[0]
        efs_ids = [str(i) for i in range(len(loc_col.collections))]

        mock_get_efs_id = mocker.patch(
            "collecte.tasks.collections.get_efs_id", side_effect=efs_ids
        )
        await tasks_collections._handle_location(loc_col)

        assert mock_get_efs_id.call_count == len(efs_ids)
        for efs_id, collection in zip(efs_ids, loc_col.collections):
            assert collection.efs_id == efs_id


class TestTransformLocationCollections:
    @pytest.mark.asyncio
    async def test_success(self, mock_loc_col, mock_col):
        location = mock_loc_col.schemas[0]

        await tasks_collections._transform_location_collections(location)

        for collection in location.collections:
            assert isinstance(collection, CollectionGroupSchema)


class TestUpdateCollections:
    @pytest.mark.asyncio
    async def test_success(self, mocker, mock_loc):
        mock_locations = [schema.model_dump() for schema in mock_loc.schemas[:2]]

        mock_get_collections_locations = mocker.patch(
            "collecte.tasks.collections._get_collections_locations",
            return_value=mock_locations,
        )
        mock_handle_location = mocker.patch(
            "collecte.tasks.collections._handle_location"
        )
        mock_transform_location_collections = mocker.patch(
            "collecte.tasks.collections._transform_location_collections"
        )
        mock_save_location_collections = mocker.patch(
            "collecte.tasks.collections.save_location_collections",
            return_value=(10, 5, 3),
        )

        await tasks_collections.update_collections()

        mock_get_collections_locations.assert_awaited()
        assert mock_handle_location.call_count == len(mock_locations)
        assert mock_transform_location_collections.call_count == len(mock_locations)
        mock_save_location_collections.assert_awaited_with(mock_loc.schemas[:2])

    @pytest.mark.asyncio
    async def test_empty_locations(self, mocker):
        mock_get_collections_locations = mocker.patch(
            "collecte.tasks.collections._get_collections_locations", return_value=[]
        )
        mock_handle_location = mocker.patch(
            "collecte.tasks.collections._handle_location"
        )
        mock_transform_location_collections = mocker.patch(
            "collecte.tasks.collections._transform_location_collections"
        )
        mock_save_location_collections = mocker.patch(
            "collecte.tasks.collections.save_location_collections",
            return_value=(0, 0, 0),
        )
        mock_log = mocker.patch.object(tasks_collections.logger, "error")

        await tasks_collections.update_collections()

        mock_get_collections_locations.assert_awaited()
        mock_handle_location.assert_not_called()
        mock_transform_location_collections.assert_not_called()
        mock_save_location_collections.assert_not_awaited()
        mock_log.assert_called_once()

    @pytest.mark.asyncio
    async def test_params(self, mocker: MockerFixture, mock_loc):
        mock_data = [schema.model_dump() for schema in mock_loc.schemas]

        mock_get_collections_locations = mocker.patch(
            "collecte.tasks.collections._get_collections_locations"
        )
        mock_handle_location = mocker.patch(
            "collecte.tasks.collections._handle_location"
        )
        mock_transform_location_collections = mocker.patch(
            "collecte.tasks.collections._transform_location_collections"
        )
        mock_save_location_collections = mocker.patch(
            "collecte.tasks.collections.save_location_collections",
            return_value=(0, 0, 0),
        )
        mock_log = mocker.patch.object(tasks_collections.logger, "error")

        await tasks_collections.update_collections(mock_data)

        mock_get_collections_locations.assert_not_awaited()
        assert mock_handle_location.await_count == 3
        assert mock_transform_location_collections.await_count == 3
        mock_save_location_collections.assert_awaited()
        mock_log.assert_not_called()
