import pytest
from unittest.mock import patch, MagicMock
import requests
from updaters.us.interfaces import Frequency
from updaters.us.fred import collectors
from updaters.libs import exceptions


class TestSetLimitOfReadings:

    def test_frequency_daily(self, period_limits):
        limit = collectors.set_limit_of_readings(
            frequency=Frequency.DAILY,
            period_limits=period_limits
        )
        assert limit == 252

    def test_frequency_weekly(self, period_limits):
        limit = collectors.set_limit_of_readings(
            frequency=Frequency.WEEKLY,
            period_limits=period_limits
        )
        assert limit == 104

    def test_frequency_monthly(self, period_limits):
        limit = collectors.set_limit_of_readings(
            frequency=Frequency.MONTHLY,
            period_limits=period_limits
        )
        assert limit == 60

    def test_frequency_quarterly(self, period_limits):
        limit = collectors.set_limit_of_readings(
            frequency=Frequency.QUARTERLY,
            period_limits=period_limits
        )
        assert limit == 40


class TestGetConstituentUrl:

    def test_valid_url(self, test_fred_base_url):
        code = "gdp"
        limit = 2
        api_key = "fake_api_key"

        url = collectors.get_constituent_url(
            code, limit, test_fred_base_url, api_key
            )
        
        assert url == (
            f"https://test_fred_base_url/gdp&api_key=fake_api_key"
            f"&sort_order=desc&limit=2&file_type=json"
            )

class TestFetchConstituentData:

    @patch(target="updaters.us.fred.collectors.requests")
    def test_fetch_constituent_data_positive(self, mock_requests):
        
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {"foo": "bar"}
        mock_requests.get.return_value = mock_response

        result = collectors.fetch_constituent_data("fake_url")
        assert result["foo"] == "bar"
        assert "foo" in result.keys()
        
    @patch(target="updaters.us.fred.collectors.requests")
    def test_fetch_constituent_data_negative(self, mock_requests):
        mock_response = MagicMock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.HTTPError
        mock_requests.get.return_value = mock_response

        with pytest.raises(requests.exceptions.RequestException):
            collectors.fetch_constituent_data("fake_url")


class TestParseConstituentData:
    
    def test_correct_data_from_api_two_values(self):
        raw_data = {
            "key1": "val1",
            "key2": "val2",
            "observations": [
                {"k1": "v1", "k2": "v2", "date": "2021-01-01", "value": "101.001"},
                {"k1": "v1", "k2": "v2", "date": "2021-02-01", "value": "102.002"},
                {"k1": "v1", "k2": "v2", "date": "2021-03-01", "value": "."},
                ]
            }
        result = collectors.parse_constituent_data(raw_data)
        expected = {"2021-01-01": 101.001, "2021-02-01": 102.002}

        assert result == expected

    def test_correct_data_from_api_but_empty(self):
        raw_data = {
            "key1": "val1",
            "key2": "val2",
            "observations": [
                {"k1": "v1", "k2": "v2", "date": "2021-01-01", "value": "."},
                {"k1": "v1", "k2": "v2", "date": "2021-02-01", "value": "."},
                {"k1": "v1", "k2": "v2", "date": "2021-03-01", "value": "."},
                ]
            }
        result = collectors.parse_constituent_data(raw_data)
        expected = {}

        assert result == expected

    def test_incorrect_data_from_api_obaservations_empty(self):
        raw_data = {
            "key1": "val1",
            "key2": "val2",
            "observations": []
            }

        with pytest.raises(exceptions.FredApiNoObservationsDataException):
            collectors.parse_constituent_data(raw_data)

    def test_incorrect_data_from_api_no_obaservations(self):
        raw_data = {
            "key1": "val1",
            "key2": "val2",
            }

        with pytest.raises(exceptions.FredApiNoObservationsDataException):
            collectors.parse_constituent_data(raw_data)