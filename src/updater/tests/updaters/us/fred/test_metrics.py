import pytest
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from db.base_class import Base
from updaters.us.fred import metrics
from updaters.libs import exceptions
from updaters.us.fred.metrics_plugins import metric_housing


class TestGetMetricsFromPlugins:

    def test_positive(self):
        plugins_path = 'tests/updaters/us/fred/fake_metrics_plugins_not_empty'
        res = metrics.get_metrics_from_plugins(plugins_path)

        assert len(res) == 1        
        assert res[0].code == 'gdp'
        assert 'Real GDP' in res[0].constituents.values()

    def test_negative_wrong_path(self):
        plugins_path = 'wrong/path'

        with pytest.raises(exceptions.FredMetricPluginNotFoundException):
            metrics.get_metrics_from_plugins(plugins_path)

    def test_negative_no_plugins(self):
        plugins_path = 'tests/updaters/us/fred/fake_metrics_plugins_empty'
        res = metrics.get_metrics_from_plugins(plugins_path)

        assert len(res) == 0


class TestExtractMetricMetadata:

    def test_positive(self):
        plugins_path = 'tests/updaters/us/fred/fake_metrics_plugins_not_empty'
        res = metrics.get_metrics_from_plugins(plugins_path)[0]
        res_metadata = metrics.extract_metric_metadata(res)
        
        assert isinstance(res_metadata, dict)
        assert len(res_metadata) == 5
        assert 'code' in res_metadata


class HousingTable(Base):
    __tablename__ = "us_housing_data"
    date: Mapped[str] = mapped_column(primary_key=True)
    permits: Mapped[float]
    started: Mapped[float]
    completed: Mapped[float]


class TestFindLastMetricDataDateInDb:
    engine = create_engine("sqlite:///:memory:")

    def test_table_at_least_two_rows(self):
        
        Session = sessionmaker(self.engine)
        Base.metadata.create_all(self.engine)

        with Session() as session:
            session.execute(
                insert(HousingTable),
                [
                    {
                        "date": "2023-01-01",
                        "permits": 100,
                        "started": 200,
                        "completed": 300
                        },
                    {
                        "date": "2023-02-01",
                        "permits": 101,
                        "started": 201,
                        "completed": 301
                        },
                    {
                        "date": "2023-03-01",
                        "permits": 102,
                        "started": 202,
                        "completed": 302
                        },
                        ]
                        )
            session.commit()

        with Session().connection() as conn:
            housing_obj = metric_housing.Metric()
            last_date = metrics.find_last_metric_data_date_in_db(
                housing_obj, conn
                )
            
        assert last_date == "2023-03-01"
    
    def test_negative(self):
        plugins_path = 'tests/updaters/us/fred/fake_metrics_plugins_not_empty'
        metric_obj = metrics.get_metrics_from_plugins(plugins_path)[0]
        
        with self.engine.connect() as conn:
            with pytest.raises(exceptions.NoTableFoundException):
                metrics.find_last_metric_data_date_in_db(metric_obj, conn)