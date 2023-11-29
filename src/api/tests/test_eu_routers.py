from db.base import get_db
from .tester_db import engine, override_get_db
from main import app
from fastapi import HTTPException
from fastapi.testclient import TestClient
from .models import Base
from.conftest import get_fake_base_api_url
import pytest
from routers.eu import get_base_api_url

# from faker import Faker
# from faker.providers import internet

# fake = Faker()
# fake.add_provider(internet)

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
        assert data["esi"]["url"] == "https://test_base_api_url/eu/metric/esi"
        assert data["esi"]["url_data"] == "https://test_base_api_url/eu/metric/esi/data"
        assert data["esi"]["url_stats"] == "https://test_base_api_url/eu/metric/esi/stats"
        assert data["indu"]["code"] == "indu"
        assert data["indu"]["url"] == "https://test_base_api_url/eu/metric/indu"
        assert data["indu"]["url_data"] == "https://test_base_api_url/eu/metric/indu/data"
        assert data["indu"]["url_stats"] == "https://test_base_api_url/eu/metric/indu/stats"

    def test_no_metrics_tables_in_db(self):
        response = client.get("eu/metrics")
        
        assert response.status_code == 404
        assert response.json().get("detail") == "No metric's table found."

