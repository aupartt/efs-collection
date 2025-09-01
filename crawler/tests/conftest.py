from pathlib import Path
from unittest.mock import MagicMock

import pytest
from crawlee.crawlers import BeautifulSoupCrawlingContext

TEST_DATA_DIR = Path(__file__).parent / "test_data"


@pytest.fixture()
def _mock_context():
    def sub(soup=None, url="http://foo.bar"):
        mock_request = MagicMock(url=url)
        mock_context = MagicMock(BeautifulSoupCrawlingContext, request=mock_request)
        if soup:
            mock_context.soup = soup
        return mock_context

    return sub
