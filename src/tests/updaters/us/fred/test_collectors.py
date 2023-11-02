from unittest.mock import patch, MagicMock
from unittest import TestCase
import datetime
import requests
from updaters.us.interfaces import Frequency
from updaters.us.fred import collectors
from updaters.us import exceptions


class TestSetFredApiStartDate:

    @patch("datetime.date")
    def test_frequency_daily(self, mock_date):
        mock_date.today.return_value = datetime.datetime.strptime("2023-11-01", "%Y-%m-%d")
        result_date = collectors.set_fred_api_start_date(
            frequency=Frequency.DAILY,
            start_date="2020-01-01",
            days_back="1",
            weeks_back="4",
        )
        assert result_date == "2023-10-31"

    @patch("datetime.date")
    def test_frequency_weekly(self, mock_date):
        mock_date.today.return_value = datetime.datetime.strptime("2023-10-31", "%Y-%m-%d")
        result_date = collectors.set_fred_api_start_date(
            frequency=Frequency.WEEKLY,
            start_date="2020-01-01",
            days_back="1",
            weeks_back="4",
        )
        assert result_date == "2023-10-03"

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

        with TestCase().assertRaises(
            exceptions.FredApiNoObservationsDataException
            ):
            collectors.parse_constituent_data(raw_data)

    def test_incorrect_data_from_api_no_obaservations(self):
        raw_data = {
            "key1": "val1",
            "key2": "val2",
            }

        with TestCase().assertRaises(
            exceptions.FredApiNoObservationsDataException
            ):
            collectors.parse_constituent_data(raw_data)