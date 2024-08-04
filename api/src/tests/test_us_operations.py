import pytest
from db.base_class import Base
from us import operations
from libs import exceptions
from tests.tester_db import engine


class TestGetMetricDataFromDb:

    def test_table_exists(self, db_us):
        table = operations.get_metric_data_from_db('housing', limit=0, db=db_us)

        assert isinstance(table, dict)
        assert table['permits']['2023-01-01'] == 100
    
    def test_table_not_exists(self, db_us):
        Base.metadata.drop_all(engine)
        
        with pytest.raises(exceptions.NoTableFoundException):
            operations.get_metric_data_from_db('housing', limit=0, db=db_us)


class TestGetMetricStatisticsFromDb:

    def test_table_exists(self, db_us):
        table = operations.get_metric_statistics_from_db('housing', db=db_us)

        assert isinstance(table, dict)
        assert table['permits']['percentile'] == 200
        assert table['started']['last/previous'] == 204
        assert table['completed']
    
    def test_table_not_exists(self, db_us):
        Base.metadata.drop_all(engine)
        
        with pytest.raises(exceptions.NoTableFoundException):
            operations.get_metric_statistics_from_db('housing', db_us)


class TestGetMetricMetadataFromDb:

    def test_metric_table_exists(self, db_us):
        metadata = operations.get_metric_metadata_from_db('housing', db_us)

        assert isinstance(metadata, dict)
        assert metadata["name"] == "Housing"
        assert "frequency" in metadata

    def test_table_not_exists(self, db_us):
        Base.metadata.drop_all(engine)
        
        with pytest.raises(exceptions.NoTableFoundException):
            operations.get_metric_statistics_from_db('housing', db_us)


class TestMetricEndpointUrlToMetadata:

    def test_metric_metadata_exists(self, db_us, base_api_url):
        metadata = operations.get_metric_metadata_from_db('housing', db_us)

        metadata = operations.add_metric_endpoint_url_to_metadata(
            metadata, base_api_url
        )

        assert metadata["url"] == f"{base_api_url}/us/metric/housing/metadata"


class TestGetMetricAllInfoFromDb:

    def test_metric_tables_exist(self, db_us, base_api_url):
        metric_info = operations.get_metric_all_info_from_db(
            "housing", 0, base_api_url, db_us
        )
        assert metric_info["metadata"]["name"] == "Housing"
        assert [*metric_info["data"]] == ["permits", "started", "completed"]


class TestCreateEndpointsToMetricsData:

    def test_table_exists(self, db_us, base_api_url):
        metrics = operations.create_endpoints_to_metrics_data(
            db_us, base_api_url
        )
        assert "housing" in metrics
        assert "url" in metrics["housing"]
        assert "url_metadata" in metrics["housing"]
        assert "url_data" in metrics["housing"]
        assert "url_stats" in metrics["housing"]
    
    def test_table_not_exists(self, db_us, base_api_url):
        Base.metadata.drop_all(engine)

        with pytest.raises(exceptions.NoTableFoundException):
            operations.create_endpoints_to_metrics_data(db_us, base_api_url)