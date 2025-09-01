from unittest.mock import MagicMock

import pytest
from bs4 import BeautifulSoup
from crawlee.crawlers import BeautifulSoupCrawlingContext
from pytest_mock import MockerFixture

import crawler.parsers.location as parsers
from crawler.models import Result


@pytest.fixture()
def _mock_context():
    def sub(soup=None):
        mock_request = MagicMock(url="http://foo.bar")
        mock_context = MagicMock(BeautifulSoupCrawlingContext, request=mock_request)
        if soup:
            mock_context.soup = soup
        return mock_context

    return sub


@pytest.mark.asyncio
async def test_parse_location_success(mocker: MockerFixture, _mock_context):
    mock_context = _mock_context()
    mock_context.soup.select_one.return_value = MagicMock(text="FOO")

    result = await parsers.parse_location(mock_context)

    mock_context.soup.select_one.assert_called_once()
    assert isinstance(result, Result)
    assert result.success
    assert result.value == "FOO"


@pytest.mark.asyncio
async def test_parse_location_error(mocker: MockerFixture, _mock_context):
    mock_context = _mock_context()
    mock_context.soup.select_one.return_value = None

    result = await parsers.parse_location(mock_context)

    mock_context.soup.select_one.assert_called_once()
    assert isinstance(result, Result)
    assert not result.success
    assert result.error == "NO_LOCATION_FOUND"


@pytest.mark.asyncio
async def test_translate_collect_type_succes(mocker: MockerFixture):
    result = await parsers._translate_collect_type("sang")

    assert isinstance(result, Result)
    assert result.success
    assert result.value == "blood"


@pytest.mark.asyncio
async def test_translate_collect_type_error(mocker: MockerFixture):
    result = await parsers._translate_collect_type("foo")

    assert isinstance(result, Result)
    assert not result.success
    assert result.error == "UNKNOWN_COLLECT_TYPE"


@pytest.mark.asyncio
async def test_parse_collect_type_success(mocker: MockerFixture, _mock_context):
    mock_html = "<html><div id='map-timeslot__don-type'><select><option value='Sang' selected></option><option value='Plasma'></option></select></div></html>"
    soup = BeautifulSoup(mock_html, "html.parser")
    mock_context = _mock_context(soup)

    result = await parsers.parse_collect_type(mock_context)

    assert isinstance(result, Result)
    assert result.success
    assert result.value == "blood"


@pytest.mark.asyncio
async def test_parse_collect_type_error(mocker: MockerFixture, _mock_context):
    mock_html = "<html><div id='map-timeslot__don-type'><select></select></div></html>"
    soup = BeautifulSoup(mock_html, "html.parser")
    mock_context = _mock_context(soup)

    result = await parsers.parse_collect_type(mock_context)

    assert isinstance(result, Result)
    assert not result.success
    assert result.error == "COLLECT_TYPE_NOT_FOUND"
