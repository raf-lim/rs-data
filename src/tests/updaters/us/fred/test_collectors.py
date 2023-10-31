from datetime import date, timedelta
from updaters.us.interfaces import Frequency
from updaters.us.fred import collectors


def test_set_fred_api_start_date_daily():
    result_date = collectors.set_fred_api_start_date(
        frequency=Frequency.DAILY,
        start_date="2020-01-01",
        days_back="1",
        weeks_back="4",
    )
    assert result_date == str(date.today() - timedelta(days=1))


def test_set_fred_api_start_date_weekly():
    result_date = collectors.set_fred_api_start_date(
        frequency=Frequency.WEEKLY,
        start_date="2020-01-01",
        days_back="1",
        weeks_back="4",
    )
    assert result_date == str(date.today() - timedelta(weeks=4))


def test_set_fred_api_start_date_monthly():
    result_date = collectors.set_fred_api_start_date(
        frequency=Frequency.MONTHLY,
        start_date="2020-01-01",
        days_back="1",
        weeks_back="4",
    )
    assert result_date == "2020-01-01"


def test_set_fred_api_start_date_quarterly():
    result_date = collectors.set_fred_api_start_date(
        frequency=Frequency.QUARTERLY,
        start_date="2020-01-01",
        days_back="1",
        weeks_back="4",
    )
    assert result_date == "2020-01-01"
