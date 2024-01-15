from fastapi.testclient import TestClient
from db.base import get_db
from eu.routers import get_base_api_url
from main import app
from tests.tester_db import override_get_db
from conftest import get_fake_base_api_url


def override_get_base_api_url():
    return get_fake_base_api_url()


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_base_api_url] = override_get_base_api_url

client = TestClient(app)


class TestGetMetricsMetadata:

    def test_metrics_tables_exist_in_db(self, db):
        response = client.get("eu/metrics")
        data = response.json()
        assert response.status_code == 200
        assert data["esi"]["code"] == "esi"
        assert data["esi"]["url"] == (
            "https://test_base_api_url/eu/metric/esi"
            )
        assert data["esi"]["url_data"] == (
            "https://test_base_api_url/eu/metric/esi/data"
            )
        assert data["esi"]["url_stats"] == (
            "https://test_base_api_url/eu/metric/esi/stats"
            )
        assert data["indu"]["code"] == "indu"
        assert data["indu"]["url"] == (
            "https://test_base_api_url/eu/metric/indu"
            )
        assert data["indu"]["url_data"] == (
            "https://test_base_api_url/eu/metric/indu/data"
            )
        assert data["indu"]["url_stats"] == (
            "https://test_base_api_url/eu/metric/indu/stats"
            )

    def test_no_metrics_tables_in_db(self):
        response = client.get("eu/metrics")
        
        assert response.status_code == 404
        assert response.json().get("detail") == "No metric's table found."


class TestMetricAllData:

    def test_metrics_tables_exists(self, db):
        response = client.get("eu/metric/esi")
        data = response.json()

        assert response.status_code == 200
        assert data["metadata"]["code"] == "esi"
        assert data["metadata"]["url"] == (
            "https://test_base_api_url/eu/metric/esi"
            )
        assert data["metadata"]["url_data"] == (
            "https://test_base_api_url/eu/metric/esi/data"
            )
        assert data["metadata"]["url_stats"] == (
            "https://test_base_api_url/eu/metric/esi/stats"
            )
        assert data["data"]["PL_ESI"] == {
            "2023-01-01" : 11, "2023-02-01": 12,
            }
        assert data["data"]["FR_ESI"] == {
            "2023-01-01" : None, "2023-02-01": None,
            }
        assert data["data"]["DK_ESI"] == {
            "2023-01-01" : None, "2023-02-01": None,
            }
        assert data["statistics"]["PL_ESI"] == {
            "percentile": 111, "last-previous": 112,
            }
        assert data["statistics"]["FR_ESI"] == {
            "percentile": None, "last-previous": None,
            }
        assert data["statistics"]["DK_ESI"] == {
            "percentile": None, "last-previous": None,
            }

    def test_metrics_tables_exists_limit(self, db):
        response = client.get("eu/metric/esi?limit=1")
        data = response.json()

        assert response.status_code == 200
        assert data["metadata"]["code"] == "esi"
        assert data["metadata"]["url"] == (
            "https://test_base_api_url/eu/metric/esi"
            )
        assert data["metadata"]["url_data"] == (
            "https://test_base_api_url/eu/metric/esi/data"
            )
        assert data["metadata"]["url_stats"] == (
            "https://test_base_api_url/eu/metric/esi/stats"
            )
        assert data["data"]["PL_ESI"] == {"2023-02-01" : 12}
        assert data["data"]["FR_ESI"] == {"2023-02-01": None}
        assert data["data"]["DK_ESI"] == {"2023-02-01": None}
        assert data["statistics"]["PL_ESI"] == {
            "percentile": 111, "last-previous": 112,
            }
        assert data["statistics"]["FR_ESI"] == {
            "percentile": None, "last-previous": None,
            }
        assert data["statistics"]["DK_ESI"] == {
            "percentile": None, "last-previous": None,
            }
    
    def test_no_metric_tables_exists(self):
        response = client.get("eu/metric/esi")

        assert response.status_code == 404
        assert response.json()["detail"] == "Not Found"


class TestGetMetricData:

    def test_table_exists(self, db):
        response = client.get("eu/metric/esi/data")
        data = response.json()

        assert response.status_code == 200
        assert data["PL_ESI"] == {"2023-01-01" : 11, "2023-02-01": 12}
        assert data["FR_ESI"] == {"2023-01-01" : None, "2023-02-01": None}
        assert data["DK_ESI"] == {"2023-01-01" : None, "2023-02-01": None}

    def test_table_exists_limit(self, db):
        response = client.get("eu/metric/esi/data?limit=1")
        data = response.json()

        assert response.status_code == 200
        assert data["PL_ESI"] == {"2023-02-01": 12}
        assert data["FR_ESI"] == {"2023-02-01": None}
        assert data["DK_ESI"] == {"2023-02-01": None}

    def test_no_metric_tables_exists(self):
        response = client.get("eu/metric/esi/data")

        assert response.status_code == 404
        assert response.json()["detail"] == "Not Found"


class TestGetMetricStats:

    def test_table_exists(self, db):
        response = client.get("eu/metric/esi/stats")
        data = response.json()

        assert response.status_code == 200
        assert data["PL_ESI"] == {"percentile" : 111, "last-previous": 112}
        assert data["FR_ESI"] == {"percentile" : None, "last-previous": None}
        assert data["DK_ESI"] == {"percentile" : None, "last-previous": None}

    def test_no_metric_tables_exists(self):
        response = client.get("eu/metric/esi/stats")

        assert response.status_code == 404
        assert response.json()["detail"] == "Not Found"


class TestGetCountiresCodes:

    def test_table_exists(self, db):
        response = client.get("eu/countries")
        data = response.json()

        assert response.status_code == 200
        assert sorted(data) == sorted(["pl", "fr", "dk"])

    def test_no_metric_tables_exists(self):
        response = client.get("eu/countries")

        assert response.status_code == 404
        assert response.json()["detail"] == "No country's table found."


class TestGetCountryData:

    def test_table_exists(self, db):
        response = client.get("eu/country/pl/data")
        data = response.json()

        assert response.status_code == 200
        assert data["PL_ESI"] == {"2023-03-01" : None, "2023-04-01": None}
        assert data["PL_INDU"] == {"2023-03-01" : 13, "2023-04-01": 14}

    def test_table_exists_limit(self, db):
        response = client.get("eu/country/pl/data?limit=1")
        data = response.json()

        assert response.status_code == 200
        assert data["PL_ESI"] == {"2023-04-01": None}
        assert data["PL_INDU"] == {"2023-04-01": 14}

    def test_no_metric_tables_exists(self):
        response = client.get("eu/country/pl/data")

        assert response.status_code == 404
        assert response.json()["detail"] == "Not Found"


class TestGetCountryStats:

    def test_table_exists(self, db):
        response = client.get("eu/country/pl/stats")
        data = response.json()

        assert response.status_code == 200
        assert data["PL_ESI"] == {"percentile" : 111, "last-previous": 112}
        assert data["PL_INDU"] == {"percentile" : 211, "last-previous": 212}

    def test_no_country_tables_exists(self, db_country_stats):
        response = client.get("eu/country/pl/stats")

        assert response.status_code == 404
        assert response.json()["detail"] == "No country's table found."

    def test_no_metric_tables_exists(self):
        response = client.get("eu/country/pl/stats")

        assert response.status_code == 404
        assert response.json()["detail"] == "No metric's table found."