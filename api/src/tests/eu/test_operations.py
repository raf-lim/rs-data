import pytest
from db.base_class import Base
from eu import operations
from libs import exceptions
from tests.tester_db import engine


class TestExtractMetricsCodesFromDb:
    
    def test_tables_exist(self, db):
        tables = operations.extract_metrics_codes_from_db(db)

        assert len(tables) == 3
        assert sorted(tables) == sorted(["esi", "indu", "serv"])

    def test_no_tables(self, db):
        Base.metadata.drop_all(engine)
        with pytest.raises(exceptions.NoEuMetricTableFoundException):
            operations.extract_metrics_codes_from_db(db)


class TestGetMetricDataFromDb:

    def test_table_exists(self, db):
        data = operations.get_metric_data_from_db("esi", 0, db)
        assert isinstance(data, dict)
        assert data.get("PL_ESI") == {"2023-01-01": 11, "2023-02-01": 12}

    def test_no_table(self, db):
        Base.metadata.drop_all(engine)
        with pytest.raises(exceptions.NoTableFoundException):
            operations.get_metric_data_from_db("esi", 0, db)


class TestGetMetricStatsFromDb:

    def test_table_exists(self, db):
        data = operations.get_metric_statistics_from_db("esi", db)

        assert isinstance(data, dict)
        assert data.get("PL_ESI") == {"percentile": 111, "last-previous": 112}

    def test_no_table(self, db):
        Base.metadata.drop_all(engine)

        with pytest.raises(exceptions.NoTableFoundException):
            operations.get_metric_statistics_from_db("pl_one", db)


class TestCreateMetricMetadata:
    
    def test_metric_exists(self, base_api_url):
        metric_code = "esi"
        meta = operations.create_metric_metadata(metric_code, base_api_url)

        assert "esi" in meta.values()
        assert "https://test_base_api_url/eu/metric/esi" in meta.values()
        assert "https://test_base_api_url/eu/metric/esi/data" in meta.values()
        assert "https://test_base_api_url/eu/metric/esi/stats" in meta.values()


class TestGetMetricAllInfo:

    def test_metric_table_exists(self, base_api_url, db):
        all_info = operations.get_metric_all_info(base_api_url, "esi", 0, db)

        assert all_info["metadata"]["code"] == "esi"
        assert all_info["metadata"]["url"] == (
            "https://test_base_api_url/eu/metric/esi"
            )
        assert all_info["metadata"]["url"] == (
            "https://test_base_api_url/eu/metric/esi"
            )
        assert all_info["metadata"]["url_data"] == (
            "https://test_base_api_url/eu/metric/esi/data"
            )
        assert all_info["metadata"]["url_stats"] == (
            "https://test_base_api_url/eu/metric/esi/stats"
            )
        assert all_info["data"]["PL_ESI"] == {"2023-01-01": 11, "2023-02-01": 12}
        assert all_info["statistics"]["PL_ESI"] == {"percentile": 111, "last-previous": 112}
        

class TestCreateAllMetricsMetadata:
    
    def test_metrics_exist(self, base_api_url, db): 
        Base.metadata.create_all(engine)
        metrics_getter = operations.extract_metrics_codes_from_db
        metadata_creator = operations.create_metric_metadata
        metas = operations.create_all_metrics_metadata(
            db, base_api_url, metrics_getter, metadata_creator
            )

        assert {"esi", "indu", "serv"}.intersection(
            set(metas.keys())
            ) == {"esi", "indu", "serv"}
        assert metas["esi"]["code"] == "esi"
        assert metas["indu"]["url"] == ("https://test_base_api_url/eu/metric/indu")


class TestExtractCountriesCodesFromDb:
    
    def test_tables_exist(self, db):
        tables = operations.extract_countries_codes_from_db(db)

        assert len(tables) == 3
        assert sorted(tables) == sorted(["dk", "fr", "pl"])

    def test_no_tables(self, db):
        Base.metadata.drop_all(engine)
        with pytest.raises(exceptions.NoEuCountryTableFoundException):
            operations.extract_countries_codes_from_db(db)


class TestGetCountryDataFromDb:
    
    def test_table_exists(self, db):
        Base.metadata.create_all(engine)
        data = operations.get_country_data_from_db("pl", 0, db)

        assert isinstance(data, dict)
        assert data.get("PL_ESI") == {"2023-03-01": None, "2023-04-01": None}
        assert data.get("PL_INDU") == {"2023-03-01": 13, "2023-04-01": 14}

    def test_no_table(self, db):
        Base.metadata.drop_all(engine)

        with pytest.raises(exceptions.NoTableFoundException):
            operations.get_country_data_from_db("pl", 0, db)


class TestGetCountryStatsFromDb:
    
    def test_table_exists(self, db):
        metrics_getter = operations.extract_metrics_codes_from_db
        data = operations.get_country_statistics_from_db("pl", db, metrics_getter)

        assert isinstance(data, dict)
        assert data.get("PL_ESI") == {"percentile": 111, "last-previous": 112}
        assert data.get("PL_INDU") == {"percentile": 211, "last-previous": 212}


    def test_no_stats_tables(self, db_country_stats):
        metrics_getter = operations.extract_metrics_codes_from_db

        with pytest.raises(exceptions.NoEuCountryTableFoundException):
            operations.get_country_statistics_from_db("pl", db_country_stats, metrics_getter)


    def test_no_metrics_table(self, db):
        Base.metadata.drop_all(engine)
        metrics_getter = operations.extract_metrics_codes_from_db

        with pytest.raises(exceptions.NoEuMetricTableFoundException):
            operations.get_country_statistics_from_db("pl", db, metrics_getter)

        
