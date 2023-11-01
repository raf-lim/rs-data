from unittest.mock import patch, MagicMock
from unittest import TestCase
import requests
from updaters.us.interfaces import Frequency
from updaters.us.fred import collectors


class TestSetFredApiStartDate:

    @patch("datetime.date")
    def test_frequency_daily(self, mock_date):
        mock_date.today.return_value = "2023-11-01"
        result_date = collectors.set_fred_api_start_date(
            frequency=Frequency.DAILY,
            start_date="2020-01-01",
            days_back="1",
            weeks_back="4",
        )
        assert result_date == "2023-10-31"

    @patch("datetime.date")
    def test_frequency_weekly(self, mock_date):
        mock_date.today.retutn_value = "2023-10-31"
        result_date = collectors.set_fred_api_start_date(
            frequency=Frequency.WEEKLY,
            start_date="2020-01-01",
            days_back="1",
            weeks_back="4",
        )
        assert result_date == "2023-10-04"

    @patch("datetime.date")
    def test_frequency_monthly(self, mock_date):
        mock_date.today.return_value = "2023-11-01"
        result_date = collectors.set_fred_api_start_date(
            frequency=Frequency.MONTHLY,
            start_date="2020-01-01",
            days_back="1",
            weeks_back="4",
        )
        assert result_date == "2020-01-01"

    @patch("datetime.date")
    def test_frequency_quarterly(self, mock_date):
        mock_date.today.return_value = "2023-11-01"
        result_date = collectors.set_fred_api_start_date(
            frequency=Frequency.QUARTERLY,
            start_date="2020-01-01",
            days_back="1",
            weeks_back="4",
        )
        assert result_date == "2020-01-01"


class TestFetchConstituentData:

    @patch(target="updaters.us.fred.collectors.requests")
    def test_fetch_constituent_data_positive(self, mock_requests):
        
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {"foo": "bar"}
        mock_requests.get.return_value = mock_response
        
        result = collectors.fetch_constituent_data("foo", "bar")
        
        assert result["foo"] == "bar"
        assert "foo" in result.keys()
        
    @patch(target="updaters.us.fred.collectors.requests")
    def test_fetch_constituent_data_negative(self, mock_requests):
        
        mock_response = MagicMock(status_code=403)
        mock_requests.get.return_value = mock_response

        collectors.fetch_constituent_data("foo", "bar")
        TestCase().assertRaises(requests.HTTPError)
            
    @patch(target="updaters.us.fred.collectors.requests")
    def test_fetch_constituent_data_negative_by_AI(self, mock_requests):
        
        mock_response = MagicMock(status_code=403)
        mock_response.raise_for_status.side_effect = requests.HTTPError
        
        mock_requests.get.return_value = mock_response

        with TestCase().assertRaises(requests.HTTPError):
            collectors.fetch_constituent_data("foo", "bar")