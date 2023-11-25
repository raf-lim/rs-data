from sqlalchemy.orm import sessionmaker, Mapped 
from sqlalchemy import create_engine, StaticPool, Column, String, Float
import pytest

from db.base_class import Base
from operations import eu
from libs import exceptions

SQLALCHEMY_TEST_DB = "sqlite:///:memory:"

engine = create_engine(
        SQLALCHEMY_TEST_DB,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
        )

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        database = TestSessionLocal()
        yield database
    finally:
        database.close()


def metric_data_table_factory(metric_name: str):
    """Create metric table class dynamically."""
    table_name = f"eu_metric_{metric_name.lower()}_data"
    class_name = f"{metric_name.title()}MetricDataTable"

    GenericTable = type(class_name, (Base,), {
        "__tablename__": table_name,
        "date": Column(String, primary_key=True),
        metric_name: Column(Float)
        })
    GenericTable.date: Mapped[str]
    
    return GenericTable


def metric_stats_table_factory(metric_name: str, country_code: str):
    """Create metric table class dynamically."""
    table_name = f"eu_metric_{metric_name.lower()}_stats"
    class_name = f"{metric_name.title()}MetricStatsTable"

    GenericTable = type(class_name, (Base,), {
        "__tablename__": table_name,
        "index": Column(String, primary_key=True),
        f"{country_code}_{metric_name}".upper(): Column(Float)
        })
    GenericTable.date: Mapped[str]
    
    return GenericTable 


def country_data_table_factory(country_code: str):
    """Create country table class dynamically."""
    table_name = f"eu_country_{country_code.lower()}_data"
    class_name = f"{country_code.title()}CountryDataTable"

    GenericTable = type(class_name, (Base,), {
        "__tablename__": table_name,
        "date": Column(String, primary_key=True),
        f"{country_code.upper()}_ONE": Column(Float),
        f"{country_code.upper()}_TWO": Column(Float)
        })
    GenericTable.date: Mapped[str]
    
    return GenericTable


@pytest.fixture
def base_api_url() -> str:
    return "https://test_base_api_url"


@pytest.fixture
def db():
    yield override_get_db()


OneMetricDataTable = metric_data_table_factory("one")
TwoMetricDataTable = metric_data_table_factory("two")
ThreeMetricDataTable = metric_data_table_factory("three")
OneMetricStatsTable = metric_stats_table_factory("one", "pl")
TwoMetricStatsTable = metric_stats_table_factory("two", "pl")
PlCountryDataTable = country_data_table_factory("pl")
FrCountryDataTable = country_data_table_factory("fr")
DkCountryDataTable = country_data_table_factory("dk")


class TestExtractMetricsCodesFromDb:
    
    def test_tables_exist(self, db):
        Base.metadata.create_all(engine)
        db = next(db)
        tables = eu.extract_metrics_codes_from_db(db)
        Base.metadata.drop_all(engine)

        assert len(tables) == 3
        assert sorted(tables) == sorted(["one", "two", "three"])

    def test_no_tables(self, db):
        Base.metadata.drop_all(engine)
        db = next(db)
        with pytest.raises(exceptions.NoEuMetricTableFound):
            eu.extract_metrics_codes_from_db(db)


class TestGetMetricDataFromDb:

    def test_table_exists(self, db):
        Base.metadata.create_all(engine)
        db = next(db)
        db.add(OneMetricDataTable(date="2023-01-01", one=11))
        db.add(OneMetricDataTable(date="2023-02-01", one=12))
        db.commit()
        data = eu.get_metric_data_from_db("one", 0, db)
        Base.metadata.drop_all(engine)

        assert isinstance(data, dict)
        assert data.get("one") == {"2023-01-01": 11, "2023-02-01": 12}

    def test_no_table(self, db):
        Base.metadata.drop_all(engine)
        db = next(db)
        with pytest.raises(exceptions.NoTableFoundException):
            eu.get_metric_data_from_db("one", 0, db)


class TestGetMetricStatsFromDb:

    def test_table_exists(self, db):
        Base.metadata.create_all(engine)
        db = next(db)
        db.add(OneMetricStatsTable(index="percentile", PL_ONE=111))
        db.add(OneMetricStatsTable(index="last-previous", PL_ONE=112))
        db.commit()
        data = eu.get_metric_statistics_from_db("one", db)
        Base.metadata.drop_all(engine)

        assert isinstance(data, dict)
        assert data.get("PL_ONE") == {"percentile": 111, "last-previous": 112}

    def test_get_metric_data_from_db_no_table(self, db):
        Base.metadata.drop_all(engine)
        db = next(db)

        with pytest.raises(exceptions.NoTableFoundException):
            eu.get_metric_statistics_from_db("pl_one", db)


class TestCreateMetricMetadata:
    
    def test_metric_exists(self, base_api_url):
        metric_code = "esi"
        meta = eu.create_metric_metadata(metric_code, base_api_url)

        assert "esi" in meta.values()
        assert "https://test_base_api_url/eu/metric/esi" in meta.values()
        assert "https://test_base_api_url/eu/metric/esi/data" in meta.values()
        assert "https://test_base_api_url/eu/metric/esi/stats" in meta.values()


class TestGetMetricAllInfo:

    def test_metric_table_exists(self, base_api_url, db):
        Base.metadata.create_all(engine)
        db = next(db)
        db.add(OneMetricDataTable(date="2023-01-01", one=11))
        db.add(OneMetricStatsTable(index="percentile", PL_ONE=111))
        db.commit()
        all_info = eu.get_metric_all_info(base_api_url, "one", 0, db)

        assert all_info["metadata"]["code"] == "one"
        assert all_info["metadata"]["url"] == (
            "https://test_base_api_url/eu/metric/one"
            )
        assert all_info["metadata"]["url"] == (
            "https://test_base_api_url/eu/metric/one"
            )
        assert all_info["metadata"]["url_data"] == (
            "https://test_base_api_url/eu/metric/one/data"
            )
        assert all_info["metadata"]["url_stats"] == (
            "https://test_base_api_url/eu/metric/one/stats"
            )
        assert all_info["data"]["one"] == {"2023-01-01": 11}
        assert all_info["statistics"]["PL_ONE"] == {"percentile": 111}
        

class TestCreateAllMetricsMetadata:
    
    def test_metrics_exist(self, base_api_url, db): 
        Base.metadata.create_all(engine)
        metrics_getter = eu.extract_metrics_codes_from_db
        metadata_creator = eu.create_metric_metadata
        db = next(db)
        metas = eu.create_all_metrics_metadata(
            db, base_api_url, metrics_getter, metadata_creator
            )
        Base.metadata.drop_all(engine)

        assert {"one", "two", "three"}.intersection(
            set(metas.keys())
            ) == {"one", "two", "three"}
        assert metas["one"]["code"] == "one"
        assert metas["two"]["url"] == ("https://test_base_api_url/eu/metric/two")


class TestExtractMetricsCodesFromDb:
    
    def test_tables_exist(self, db):
        Base.metadata.create_all(engine)
        db = next(db)
        tables = eu.extract_countries_codes_from_db(db)
        Base.metadata.drop_all(engine)

        assert len(tables) == 3
        assert sorted(tables) == sorted(["dk", "fr", "pl"])

    def test_no_tables(self, db):
        Base.metadata.drop_all(engine)
        db = next(db)
        with pytest.raises(exceptions.NoEuCountryTableFound):
            eu.extract_countries_codes_from_db(db)


class TestGetCountryDataFromDb:
    
    def test_table_exists(self, db):
        Base.metadata.create_all(engine)
        db = next(db)
        db.add(PlCountryDataTable(date="2023-03-01", PL_TWO=13))
        db.add(PlCountryDataTable(date="2023-04-01", PL_TWO=14))
        db.commit()
        data = eu.get_country_data_from_db("pl", 0, db)

        assert isinstance(data, dict)
        assert data.get("PL_ONE") == {"2023-03-01": None, "2023-04-01": None}
        assert data.get("PL_TWO") == {"2023-03-01": 13, "2023-04-01": 14}

    def test_no_table(self, db):
        Base.metadata.drop_all(engine)
        db = next(db)

        with pytest.raises(exceptions.NoTableFoundException):
            eu.get_country_data_from_db("pl", 0, db)


class TestGetCountryStatsFromDb:
    
    def test_table_exists(self, db):
        Base.metadata.create_all(engine)
        db = next(db)
        db.add(OneMetricStatsTable(index="percentile", PL_ONE=111))
        db.add(OneMetricStatsTable(index="last-previous", PL_ONE=112))
        db.add(TwoMetricStatsTable(index="percentile", PL_TWO=211))
        db.add(TwoMetricStatsTable(index="last-previous", PL_TWO=212))
        db.commit()

        metrics_getter = eu.extract_metrics_codes_from_db
        data = eu.get_country_statistics_from_db("pl", db, metrics_getter)
        Base.metadata.drop_all(engine)

        assert isinstance(data, dict)
        assert data.get("PL_ONE") == {"percentile": 111, "last-previous": 112}
        assert data.get("PL_TWO") == {"percentile": 211, "last-previous": 212}


    def test_no_stats_tables(self, db):
        Base.metadata.create_all(engine)
        db = next(db)
        metrics_getter = eu.extract_metrics_codes_from_db

        with pytest.raises(exceptions.NoEuCountryTableFound):
            eu.get_country_statistics_from_db("pl", db, metrics_getter)


    def test_no_metrics_table(self, db):
        Base.metadata.drop_all(engine)
        metrics_getter = eu.extract_metrics_codes_from_db
        db = next(db)

        with pytest.raises(exceptions.NoEuMetricTableFound):
            eu.get_country_statistics_from_db("pl", db, metrics_getter)

        
