import logging
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from bs4 import BeautifulSoup
from pytest_mock import MockerFixture

from crawler.handlers import collect_handler
from crawler.models import LocationEvents, Result

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture()
def mock_html():
    return """
    <html>
      <div class="card-rdv">
        <div class="top">
          Ch'Hawaii
        </div>
      </div>
      <div id='map-timeslot__don-type'>
        <select>
          <option value='Sang' selected></option>
          <option value='Plasma'></option>
          <option value='Plaquette'></option>
        </select>
      </div>
      <div>
        <div class="timeslot-item" data-date="19/09/2025">
          <div class="timeslot-item__header"><div class="place">4 places</div></div>
          <div class="time-block__item">14h25<br><span class="place">1 place</span></div>
          <div class="time-block__item">14h30<br><span class="place">2 place</span></div>
          <div class="time-block__item">14h35<br><span class="place">1 place</span></div>
        </div>
        <div class="timeslot-item" data-date="20/09/2025">
          <div class="timeslot-item__header"><div class="place">5 places</div></div>
          <div class="time-block__item">13h25<br><span class="place">2 place</span></div>
          <div class="time-block__item">13h30<br><span class="place">0 place</span></div>
          <div class="time-block__item">13h35<br><span class="place">3 place</span></div>
        </div>
      </div>
    </html>
    """

@pytest.mark.asyncio
async def test_start_crawler_success(mocker: MockerFixture, _mock_context, mock_html):
    mock_soup = BeautifulSoup(mock_html, features="html.parser")
    mock_context = _mock_context(soup=mock_soup, url="http://efscollect.fr")
    mock_context.push_data = AsyncMock()
    now = datetime.now(UTC)
    mock_datetime = mocker.patch("crawler.handlers.datetime")
    mock_datetime.now.return_value = now

    await collect_handler(mock_context)

    mock_datetime.now.assert_called_once()
    mock_context.push_data.assert_awaited_once_with(
        LocationEvents(
            **{
                "url": "http://efscollect.fr",
                "location": "Ch'Hawaii",
                "collect_type": "blood",
                "time": now.isoformat(),
                "events": [
                    {
                        "slots": 4,
                        "date": "19/09/2025",
                        "schedules": {"14h25": 1, "14h30": 2, "14h35": 1},
                    },
                    {
                        "slots": 5,
                        "date": "20/09/2025",
                        "schedules": {"13h25": 2, "13h30": 0, "13h35": 3},
                    },
                ],
            }
        ).model_dump_json()
    )

@pytest.mark.asyncio
async def test_start_crawler_error(mocker: MockerFixture, _mock_context, mock_html):
    mock_soup = BeautifulSoup(mock_html, features="html.parser")
    mock_context = _mock_context(soup=mock_soup, url="http://efscollect.fr")
    mock_context.push_data = AsyncMock()

    mocker.patch("crawler.handlers.parse_location", side_effect=Exception("foo"))

    await collect_handler(mock_context)

    mock_context.push_data.assert_not_awaited()
    mock_context.log.error.assert_called_once()


@pytest.mark.asyncio
async def test_start_crawler_failed_location(mocker: MockerFixture, _mock_context, mock_html):
    mock_soup = BeautifulSoup(mock_html, features="html.parser")
    mock_context = _mock_context(soup=mock_soup, url="http://efscollect.fr")
    mock_context.push_data = AsyncMock()

    mocker.patch("crawler.handlers.parse_location", return_value=Result(success=False, error="FOO"))

    await collect_handler(mock_context)

    mock_context.push_data.assert_not_awaited()


@pytest.mark.asyncio
async def test_start_crawler_failed_collect_type(mocker: MockerFixture, _mock_context, mock_html):
    mock_soup = BeautifulSoup(mock_html, features="html.parser")
    mock_context = _mock_context(soup=mock_soup, url="http://efscollect.fr")
    mock_context.push_data = AsyncMock()

    mocker.patch("crawler.handlers.parse_collect_type", return_value=Result(success=False, error="FOO"))

    await collect_handler(mock_context)

    mock_context.push_data.assert_not_awaited()


@pytest.mark.asyncio
async def test_start_crawler_failed_parse_events(mocker: MockerFixture, _mock_context, mock_html):
    mock_soup = BeautifulSoup(mock_html, features="html.parser")
    mock_context = _mock_context(soup=mock_soup, url="http://efscollect.fr")
    mock_context.push_data = AsyncMock()

    mocker.patch("crawler.handlers.parse_events", return_value=Result(success=False, error="FOO"))

    await collect_handler(mock_context)

    mock_context.push_data.assert_not_awaited()
