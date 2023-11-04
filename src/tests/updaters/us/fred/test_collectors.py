from unittest.mock import patch, MagicMock
from unittest import TestCase
import requests
from sqlalchemy import create_engine, text, insert, select
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from db.base_class import Base
from updaters.us.interfaces import Frequency
from updaters.us.fred import collectors
from updaters.us import exceptions
from updaters.us.fred.metrics import Housing

class TestSetLimitOfReadings:
    LIMIT_FRED_DAILY = "252"
    LIMIT_FRED_WEEKLY = "104"
    LIMIT_FRED_MONTHLY = "60"
    LIMIT_FRED_QUARTERLY = "40"

    def test_frequency_daily(self):
        limit = collectors.set_limit_of_readings(
            frequency=Frequency.DAILY,
        )
        assert limit == 252

    def test_frequency_weekly(self):
        limit = collectors.set_limit_of_readings(
            frequency=Frequency.WEEKLY,
        )
        assert limit == 104

    def test_frequency_monthly(self):
        limit = collectors.set_limit_of_readings(
            frequency=Frequency.MONTHLY,
        )
        assert limit == 60

    def test_frequency_quarterly(self):
        limit = collectors.set_limit_of_readings(
            frequency=Frequency.QUARTERLY,
        )
        assert limit == 40


class HousingTable(Base):
    __tablename__ = "us_housing_data"
    date: Mapped[str] = mapped_column(primary_key=True)
    permits: Mapped[float]
    started: Mapped[float]
    completed: Mapped[float]

class TestFindLastMetricDataDateInDb:

    def test_table_at_least_two_rows(self):
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(engine)
        Base.metadata.create_all(engine)

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
            last_date = collectors.find_last_metric_data_date_in_db(Housing, conn)
            
        assert last_date == "2023-03-01"


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