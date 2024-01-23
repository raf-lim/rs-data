import pytest
from db.base_class import Base
from tests.tester_db import engine, TestSessionLocal

from models_eu import EsiData, EsiStats, InduStats, PlData
from models_us import HousingData, HousingStats, UsMetricsMetadata


def get_fake_base_api_url() -> str:
    return "https://test_base_api_url"


def fake_eu_data():
    fake_data = [
        EsiData(date="2023-01-01", PL_ESI=11),
        EsiData(date="2023-02-01", PL_ESI=12), 
        EsiStats(stat="percentile", PL_ESI=111),
        EsiStats(stat="last-previous", PL_ESI=112),
        InduStats(stat="percentile", PL_INDU=211),
        InduStats(stat="last-previous", PL_INDU=212),
        PlData(date="2023-03-01", PL_INDU=13),
        PlData(date="2023-04-01", PL_INDU=14),
        ]
    return fake_data


def fake_us_data():
    fake_data = [
        HousingData(date="2023-01-01", permits=100, started=101, completed=102),
        HousingStats(index="2023-01-01", permits=200, started=201, completed=202),
        UsMetricsMetadata(
            code='housing', name='Housing', frequency='monthly',
            data='index', stats='change'
        )
    ]
    return fake_data


@pytest.fixture
def base_api_url():
    return get_fake_base_api_url()


@pytest.fixture
def db():
    Base.metadata.create_all(engine)
    try:
        session = TestSessionLocal()
        for data_obj in fake_eu_data():
            session.add(data_obj)
        session.commit()
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def db_us():
    Base.metadata.create_all(engine)
    try:
        session = TestSessionLocal()
        for data_obj in fake_us_data():
            session.add(data_obj)
        session.commit()
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)

