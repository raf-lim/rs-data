import os
from typing import Callable, Iterable, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np


THIS_API_BASE_URL = os.getenv("THIS_API_BASE_URL")


def extract_metrics_names_from_db(
        db: Session,
    ) -> Iterable[str]:
    """Extract EU metrics' names from tables' names in database"""
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
        metrics_getter: MetricsCodesGetterFn = extract_metrics_names_from_db,
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
        index_col="index" #TODO: might be changed later in updater into "stats"...
    )
    data = data.replace(to_replace=np.NaN, value=None)

    return data.to_dict()


def get_metric_all_info(
        metric_code: str,
        limit: int,
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
