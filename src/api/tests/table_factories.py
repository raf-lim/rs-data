from sqlalchemy import Column, String, Float
from sqlalchemy.orm import Mapped

from db.base_class import Base

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