from unittest.mock import AsyncMock, MagicMock

import pytest
from bs4 import BeautifulSoup
from pytest_mock import MockerFixture

import crawler.parsers.events as parsers
from crawler.models import Event, Result


@pytest.mark.asyncio
async def test_parse_event_date_success():
    mock_html = '<div data-date="19/09/2025"></div>'
    mock_soup = BeautifulSoup(mock_html, features="html.parser")

    date = await parsers._parse_event_date(mock_soup.select_one("div"))

    assert date == "19/09/2025"


@pytest.mark.asyncio
async def test_parse_event_date_error():
    mock_html = "<div></div>"
    mock_soup = BeautifulSoup(mock_html, features="html.parser")

    with pytest.raises(ValueError, match="EVENT_DATE_NOT_FOUND"):
        await parsers._parse_event_date(mock_soup.select_one("div"))


@pytest.mark.asyncio
async def test_parse_event_slots_success():
    mock_html = (
        '<div class="timeslot-item__header"><div class="place">10 places</div></div>'
    )
    mock_soup = BeautifulSoup(mock_html, features="html.parser")

    slots = await parsers._parse_event_slots(mock_soup.select_one("div"))

    assert slots == 10


@pytest.mark.asyncio
async def test_parse_event_slots_error():
    mock_html = (
        '<div class="timeslot-item__header"><div class="place">Closed</div></div>'
    )
    mock_soup = BeautifulSoup(mock_html, features="html.parser")

    with pytest.raises(ValueError, match="EVENT_SLOT_NOT_FOUND"):
        await parsers._parse_event_slots(mock_soup.select_one("div"))


@pytest.mark.asyncio
async def test_parse_event_schedules_success():
    mock_html = """
  <div>
    <div class="time-block__item">14h25<br><span class="place">1 place</span></div>
    <div class="time-block__item">14h30<br><span class="place">2 place</span></div>
    <div class="time-block__item">14h35<br><span class="place">1 place</span></div>
  </div>
  """
    mock_soup = BeautifulSoup(mock_html, features="html.parser")

    result = await parsers._parse_event_schedules(mock_soup.select_one("div"))

    assert result == {"14h25": 1, "14h30": 2, "14h35": 1}


@pytest.mark.asyncio
async def test_parse_event_schedules_empty():
    mock_html = """
  <div>
  </div>
  """
    mock_soup = BeautifulSoup(mock_html, features="html.parser")

    result = await parsers._parse_event_schedules(mock_soup.select_one("div"))

    assert result == {}


@pytest.mark.asyncio
async def test_parse_event_success(mocker: MockerFixture):
    mock_parse_date = mocker.patch(
        "crawler.parsers.events._parse_event_date",
        AsyncMock(return_value="19/09/2025"),
    )
    mock_parse_schedules = mocker.patch(
        "crawler.parsers.events._parse_event_schedules",
        AsyncMock(return_value={"10h00": 5, "10h05": 3}),
    )
    mock_parse_slots = mocker.patch(
        "crawler.parsers.events._parse_event_slots",
        AsyncMock(return_value=8),
    )

    result = await parsers._parse_event("http://foo.bar", MagicMock())

    mock_parse_date.assert_awaited_once()
    mock_parse_schedules.assert_awaited_once()
    mock_parse_slots.assert_awaited_once()
    assert isinstance(result, Result)
    assert result.success
    assert result.value.date == "19/09/2025"
    assert result.value.slots == 8
    assert result.value.schedules == {"10h00": 5, "10h05": 3}


@pytest.mark.asyncio
async def test_parse_event_error(mocker):
    mock_soup = BeautifulSoup("<div></div>")

    result = await parsers._parse_event("http://foo.bar", mock_soup.select_one("div"))

    assert isinstance(result, Result)
    assert not result.success
    assert result.error == "EVENT_DATE_NOT_FOUND"


@pytest.mark.asyncio
async def test_parse_events_success(mocker, _mock_context):
    mock_html = """
  <html>
    <div class="timeslot-item " data-date="19/09/2025">
      <div class="time-block__item">14h25<br><span class="place">1 place</span></div>
      <div class="time-block__item">14h30<br><span class="place">2 place</span></div>
      <div class="time-block__item">14h35<br><span class="place">1 place</span></div>
    </div>
  </html>
  """
    soup = BeautifulSoup(mock_html, "html.parser")
    mock_context = _mock_context(soup)
    mocker.patch(
        "crawler.parsers.events._parse_event",
        AsyncMock(
            return_value=Result(
                success=True,
                value=Event(
                    date="19/09/2025", slots=8, schedules={"10h00": 5, "10h05": 3}
                ),
            )
        ),
    )

    result = await parsers.parse_events(mock_context)

    assert isinstance(result, Result)
    assert result.success
    assert len(result.value) == 1
    assert result.value[0].date == "19/09/2025"


@pytest.mark.asyncio
async def test_parse_events_no_events(mocker, _mock_context):
    mock_html = "<html></html>"
    soup = BeautifulSoup(mock_html, "html.parser")
    mock_context = _mock_context(soup)

    result = await parsers.parse_events(mock_context)

    assert result is None
