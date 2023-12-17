from enum import StrEnum
import pytest
from updaters.libs.helpers import PeriodDataLimits


@pytest.fixture
def period_limits() -> PeriodDataLimits:
    class TestPeriodDataLimits(StrEnum):
        LIMIT_FRED_DAILY = "252"
        LIMIT_FRED_WEEKLY = "104"
        LIMIT_FRED_MONTHLY = "60"
        LIMIT_FRED_QUARTERLY = "40"

    return TestPeriodDataLimits


@pytest.fixture
def test_fred_base_url() -> str:
    return "https://test_fred_base_url/"