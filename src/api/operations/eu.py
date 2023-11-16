import os
from typing import Callable, Iterable, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np

THIS_API_BASE_URL = os.getenv("THIS_API_BASE_URL")


def extract_metrics_codes_from_db(
        db: Session,
    ) -> Iterable[str]:
    """Extract EU metrics' codes from tables' names in database"""
    tables = db.scalars(
        text(f"""
             SELECT table_name
             FROM information_schema.tables
             WHERE table_schema = :table_schema
             AND table_name LIKE :table_name_prefix
             AND table_name LIKE :table_name_suffix
             """), {
                 "table_schema": "public",
                 "table_name_prefix": "eu_metric%",
                 "table_name_suffix": "%data"
                 }).all()
    
    return [table_name.split("_")[-2] for table_name in tables]


def create_metric_metadata(
        metric_code: str, base_api_url: str = THIS_API_BASE_URL,
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
        metrics_getter: MetricsCodesGetterFn = extract_metrics_codes_from_db,
        metadata_creator: MetadataCreatorFn = create_metric_metadata,
        ) -> dict[str, dict[str, str]]:
    metrics_codes = metrics_getter(db)

    return {
        metric_code: metadata_creator(metric_code)
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
    data = pd.read_sql_table(
        table_name=f"eu_metric_{metric_code}_data",
        con=db.connection(),
        index_col="date"
    )[-limit:]
    data = data.replace(to_replace=np.NaN, value=None)

    return data.to_dict()


def get_metric_statistics_from_db(
        metric_code: str,
        db: Session
    ) -> dict[str, dict[str, float | None]]:
    """
    Get metric's statistics from database.
    """
    data = pd.read_sql_table(
        table_name=f"eu_metric_{metric_code}_stats",
        con=db.connection(),
        index_col="index"
    )
    data = data.replace(to_replace=np.NaN, value=None)

    return data.to_dict()


def get_metric_all_info(
        metric_code: str,
        limit: Optional[int],
        db: Session,
) -> dict[str, dict[str, str] | dict[str, dict[str, float | None]]]:
    """Get metric's data and statistics from database."""
    metadata = create_metric_metadata(metric_code)
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
    tables = db.scalars(
        text(f"""
             SELECT table_name
             FROM information_schema.tables
             WHERE table_schema = :table_schema
             AND table_name LIKE :table_name_prefix
             AND table_name LIKE :table_name_suffix
             """), {
                 "table_schema": "public",
                 "table_name_prefix": "eu_country%",
                 "table_name_suffix": "%data"
                 }).all()
    
    return (
        table_name
        .lstrip("eu")
        .lstrip("_")
        .lstrip("country")
        .lstrip("_")
        .rstrip("data")
        .rstrip("_")
          for table_name in tables
        )


def get_country_data_from_db(
        country_code: str,
        limit: Optional[int],
        db: Session
    ) -> dict[str, dict[str, float | None]]:
    """
    Get country's data from database (all constituents).
    """
    data = pd.read_sql_table(
        table_name=f"eu_country_{country_code}_data",
        con=db.connection(),
        index_col="date"
    )[-limit:]
    data = data.replace(to_replace=np.NaN, value=None)

    return data.to_dict()


def get_country_statistics_from_db(
        country_code: str,
        db: Session,
        metrics_getter: MetricsCodesGetterFn = extract_metrics_codes_from_db,
    ) -> dict[str, dict[str, float | None]]:
    """
    Get country's stats from database (all constituents).
    """
    metrics_stats: dict[str, dict[str, float | None]] = {}
    metrics_codes = metrics_getter(db)
    for metric_code in metrics_codes:
        metric_name: str = f"{country_code}-{metric_code}".upper()
        metric_stats = db.scalars(
            text(f"""
                 SELECT (index, "{metric_name}")
                 FROM eu_metric_{metric_code.lower()}_stats
                 """)
            ).all()
        metrics_stats[metric_name] = {row[0]: row[1] for row in metric_stats}

    return metrics_stats
