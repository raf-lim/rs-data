
import pytest
from db.base_class import Base
from .tester_db import engine, TestSessionLocal

from .models import (
    EsiData,
    InduData,
    ServData,
    EsiStats,
    InduStats,
    PlData,
    FrData,
    DkData,
)


@pytest.fixture
def base_api_url() -> str:
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

def fake_eu_data_for_country_stats():
    fake_data = [
        EsiData(date="2023-01-01", PL_ESI=11),
        EsiData(date="2023-02-01", PL_ESI=12),
        ]
    
    return fake_data


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
def db_country_stats():
    Base.metadata.create_all(engine)
    try:
        session = TestSessionLocal()
        for data_obj in fake_eu_data_for_country_stats():
            session.add(data_obj)
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)