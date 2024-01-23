from fastapi.testclient import TestClient
from db.base import get_db
from us.routers import get_base_api_url
from main import app
from tests.tester_db import override_get_db
from conftest import get_fake_base_api_url


def override_get_base_api_url():
    return get_fake_base_api_url()


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_base_api_url] = override_get_base_api_url

client = TestClient(app)


class TestGetMetricsDataEndpoints:

    def test_metrics_tables_exist_in_db(self, db_us, base_api_url):
        response = client.get("us/metrics")
        data = response.json()
        assert response.status_code == 200
        assert data["housing"]["code"] == "housing"
        assert data["housing"]["url"] == (
            "https://test_base_api_url/us/metric/housing"
            )
    
    def test_no_metrics_tables_in_db(self):
        response = client.get("us/metrics")
        
        assert response.status_code == 404
        assert response.json().get("detail") == "Not Found"


class TestGetMetricAllData:

    def test_metric_table_exists(self, db_us, base_api_url):
        response = client.get("us/metric/housing")
        data = response.json()
        
        assert response.status_code == 200
        assert data["metadata"]["code"] == "housing"
        assert data["metadata"]["url"] == (
            "https://test_base_api_url/us/metric/housing/metadata"
            )
        assert data["metadata"]["name"] == "Housing"
        assert data["data"]["permits"] == {"2023-01-01": 100, "2023-02-01": 103}

    def test_metric_table_exists_limit(self, db_us, base_api_url):
        response = client.get("us/metric/housing?limit=1")
        data = response.json()

        assert response.status_code == 200
        assert data["metadata"]["code"] == "housing"
        assert data["metadata"]["url"] == (
            "https://test_base_api_url/us/metric/housing/metadata"
            )
        assert data["data"]["permits"] == {"2023-02-01": 103}
        assert data["data"]["started"] == {"2023-02-01": 104}
        assert data["data"]["completed"] == {"2023-02-01": 105}
        assert data["statistics"]["permits"] == {
            "percentile": 200, "last/previous": 203,
            }
        assert data["statistics"]["started"] == {
            "percentile": 201, "last/previous": 204,
            }
        assert data["statistics"]["completed"] == {
            "percentile": 202, "last/previous": 205,
            }
    
    def test_no_metric_tables_exists(self):
        response = client.get("us/metric/housing")

        assert response.status_code == 404
        assert response.json()["detail"] == "Not Found"


class TestGetMetricMetadata:

    def test_metric_table_exists(self, db_us, base_api_url):
        response = client.get("us/metric/housing/metadata")
        metadata = response.json()

        assert response.status_code == 200
        assert metadata["code"] == "housing"
        assert metadata["url"] == (
            "https://test_base_api_url/us/metric/housing/metadata"
            )

    def test_metric_table_not_exists(self):
        response = client.get("us/metric/housing/metadata")

        assert response.status_code == 404
        assert response.json()["detail"] == "Not Found"


class TestGetMetricData:

    def test_table_exists(self, db_us):
        response = client.get("us/metric/housing/data")
        data = response.json()

        assert response.status_code == 200
        assert data["permits"] == {"2023-01-01": 100, "2023-02-01": 103}
        assert data["started"] == {"2023-01-01": 101, "2023-02-01": 104}
        assert data["completed"] == {"2023-01-01": 102, "2023-02-01": 105}

    def test_table_exists_limit(self, db_us):
        response = client.get("us/metric/housing/data?limit=1")
        data = response.json()

        assert response.status_code == 200
        assert data["permits"] == {"2023-02-01": 103}
        assert data["started"] == {"2023-02-01": 104}
        assert data["completed"] == {"2023-02-01": 105}

    def test_no_metric_tables_exists(self):
        response = client.get("us/metric/housing/data")

        assert response.status_code == 404
        assert response.json()["detail"] == "Not Found"


class TestGetMetricStats:

    def test_table_exists(self, db_us):
        response = client.get("us/metric/housing/stats")
        data = response.json()
        assert response.status_code == 200
        assert data["permits"] == {
            "percentile": 200, "last/previous": 203,
            }
        assert data["started"] == {
            "percentile": 201, "last/previous": 204,
            }
        assert data["completed"] == {
            "percentile": 202, "last/previous": 205,
            }

    def test_no_metric_tables_exists(self):
        response = client.get("us/metric/housing/stats")

        assert response.status_code == 404
        assert response.json()["detail"] == "Not Found"
