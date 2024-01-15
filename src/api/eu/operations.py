import os
from typing import Callable, Iterable, Optional
from sqlalchemy import inspect
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from libs import exceptions


def extract_metrics_codes_from_db(
        db: Session,
        ) -> Iterable[str] | None:
    """Extract EU metrics' codes from tables' names in database"""
    inspector = inspect(db.bind)
    db_tables = inspector.get_table_names()

    if len(db_tables) < 1:
        raise exceptions.NoEuMetricTableFoundException

    return [
        table.split("_")[-2]
          for table in db_tables
            if table.startswith("eu_metric") and table.endswith("data")
            ]
    

def create_metric_metadata(
        metric_code: str, base_api_url: str,
        ) -> dict[str, str]:
    """Create metadata for ESI metric."""
    url = os.path.join(base_api_url, "eu/metric", metric_code)
    metadata = {
        "code": metric_code,
        "url": url,
        "url_data": os.path.join(url, "data"),
        "url_stats": os.path.join(url, "stats")
        }

    return metadata


MetricsCodesGetterFn = Callable[[Session], Iterable[str]]
MetadataCreatorFn = Callable[[str, str], dict[str, str]]


def create_all_metrics_metadata(
        db: Session,
        base_api_url: str,
        metrics_getter: MetricsCodesGetterFn = extract_metrics_codes_from_db,
        metadata_creator: MetadataCreatorFn = create_metric_metadata,
        ) -> dict[str, dict[str, str]]:
    """Create metadata for all EU metrics in database"""
    metrics_codes = metrics_getter(db)

    return {
        metric_code: metadata_creator(metric_code, base_api_url)
          for metric_code in metrics_codes
          }


def get_metric_data_from_db(
        metric_code: str,
        limit: Optional[int],
        db: Session
        ) -> dict[str, dict[str, float | None]]:
    """
    Get metric's data from database (all constituents).
    """
    try:
        data = pd.read_sql_table(
            table_name=f"eu_metric_{metric_code}_data",
            con=db.connection(),
            index_col="date"
            )
    except ValueError:
        raise exceptions.NoTableFoundException
        
    data = data.replace(to_replace=np.NaN, value=None)

    return data[-limit:].to_dict()


def get_metric_statistics_from_db(
        metric_code: str,
        db: Session
        ) -> dict[str, dict[str, float | None]]:
    """
    Get metric's statistics from database.
    """
    try:
        data = pd.read_sql_table(
            table_name=f"eu_metric_{metric_code}_stats",
            con=db.connection(),
            index_col="stat"
            )
    except ValueError:
        raise exceptions.NoTableFoundException
    
    data = data.replace(to_replace=np.NaN, value=None)

    return data.to_dict()


def get_metric_all_info(
        base_api_url: str,
        metric_code: str,
        limit: Optional[int],
        db: Session,
) -> dict[str, dict[str, str] | dict[str, dict[str, float | None]]]:
    """Get metric's data and statistics from database."""
    metadata = create_metric_metadata(metric_code, base_api_url)
    data = get_metric_data_from_db(metric_code, limit, db)
    stats = get_metric_statistics_from_db(metric_code, db)
    
    result = {"metadata": metadata}
    result.update({"data": data})
    result.update({"statistics": stats})
    
    return result


def extract_countries_codes_from_db(
        db: Session,
        ) -> Iterable[str]:
    """Extract EU countries' codes from tables' names in database"""
    inspector = inspect(db.bind)
    db_tables = inspector.get_table_names()
    
    if len(db_tables) < 1:
        raise exceptions.NoEuCountryTableFoundException
    
    return [
        table.split("_")[-2]
          for table in db_tables
            if table.startswith("eu_country") and table.endswith("data")
            ]


def get_country_data_from_db(
        country_code: str,
        limit: Optional[int],
        db: Session
    ) -> dict[str, dict[str, float | None]]:
    """
    Get country's data from database (all constituents).
    """
    try:
        data = pd.read_sql_table(
            table_name=f"eu_country_{country_code.lower()}_data",
            con=db.connection(),
            index_col="date"
        )
    except ValueError:
        raise exceptions.NoTableFoundException
    
    data = data.replace(to_replace=np.NaN, value=None)

    return data[-limit:].to_dict()


def get_country_statistics_from_db(
        country_code: str,
        db: Session,
        metrics_getter: MetricsCodesGetterFn = extract_metrics_codes_from_db,
    ) -> dict[str, dict[str, float | None]]:
    """
    Get country's stats from database (all constituents).
    """
    metrics_stats: dict[str, dict[str, float | None]] = {}
    
    try:
        metrics_codes = metrics_getter(db)
    except exceptions.NoEuMetricTableFoundException:
        raise exceptions.NoEuMetricTableFoundException

    for metric_code in metrics_codes:
        metric_name: str = f"{country_code}_{metric_code}".upper()
        try:
            metric_stats = pd.read_sql_table(
                table_name=f"eu_metric_{metric_code.lower()}_stats",
                con=db.connection(),
                index_col="stat",
                columns=[metric_name]
                )
            metrics_stats.update(metric_stats.to_dict())
        except ValueError:
            continue
        
    # check if any stats' data for at least one metric.
    if len([stats for stats in metrics_stats.values() if len(stats) > 1]) < 1:
        raise exceptions.NoEuCountryTableFoundException

    return metrics_stats
