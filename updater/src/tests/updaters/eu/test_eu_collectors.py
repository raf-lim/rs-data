import pytest
from unittest.mock import patch, MagicMock
import requests
from updaters.eu import collectors
from updaters.libs import exceptions


class TestCompileEndpointUrl:

    def test_positive(self, fake_endpoint_url):
        country_code = "POL"
        metric_code = "INDU"
        base_url = fake_endpoint_url
        url = collectors.compile_endpoint_url(base_url, country_code, metric_code)

        assert url == "https://fake_endpoint?geo=POL&indic=INDU&s_adj=SA"


class TestFetchData:

    @patch(target="updaters.eu.collectors.requests")
    def test_positive(self, mock_requests):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {"foo": "bar"}
        mock_requests.get.return_value = mock_response

        response = collectors.fetch_data("fake_url")
        assert response["foo"] == "bar"
        assert "foo" in response

    @patch(target="updaters.eu.collectors.requests")
    def test_negative(self, mock_requests):
        mock_response = MagicMock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.HTTPError
        mock_requests.get.return_value = mock_response

        with pytest.raises(requests.exceptions.RequestException):
            collectors.fetch_data("fake_url")


class TestParseCountryMetricData:

    def test_correct_data(self):
        raw_data = {
            "value": {
                "526": -16.5,
                "527": -17.2,
            },
            "dimension": {
                "time": {
                    "category": {
                        "index": {
                            "2023-11": 526,
                            "2023-12": 527,
                        },
                    }   
                }
            }
        }
        result = collectors.parse_country_metric_data(raw_data)

        assert result.index.name == "date"
        assert result.loc["2023-11", "value"] == -16.5