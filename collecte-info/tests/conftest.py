import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def async_cm():
    def _make(return_value):
        cm = AsyncMock()
        cm.__aenter__.return_value = return_value
        cm.__aexit__.return_value = None
        return cm

    return _make
