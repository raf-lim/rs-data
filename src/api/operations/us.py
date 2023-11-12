from os import getenv
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np

BASE_API_URL = getenv("BASE_API_URL")


def create_endpoints_to_metrics_data(db: Session) -> dict[str, str]:
    """
    Create dictionary with base links to request data of available us metrics.
    End points names are derived from tables names in database.
    """
    metrics = db.scalars(
        text("""
             SELECT table_name
             FROM information_schema.tables
             WHERE table_schema = :schema;
             """
        ), {"schema": "public"}).all()
    
    metrics = sorted({
        metric
        .lstrip("us_")
        .rstrip("data")
        .rstrip("stats")
        .rstrip("_")
        .replace("_", " ")
        .title()
          for metric in metrics
    })

    metrics_with_urls: dict[str, str] = {}
    for metric in metrics:
        metrics_with_urls[metric] = (
            f"{BASE_API_URL}/us/metric/{metric.replace(' ', '_').lower()}"
        )
  
    return metrics_with_urls


def get_metric_data_from_db(
        metric_name: str,
        limit: int,
        db: Session
    ) -> dict[str, dict[str, float | None]]:
    """
    Get metric's data from database (all constituents).
    """
    data = pd.read_sql_table(
        table_name=f"us_{metric_name}_data",
        con=db.connection(),
        index_col="date"
    )[-limit:]
    data = data.replace(to_replace=np.NaN, value=None)

    return data.to_dict()


def get_metric_statistics_from_db(
        metric_name: str,
        db: Session
    ) -> dict[str, dict[str, float | None]]:
    """
    Get metric's statistics from database.
    """
    data = pd.read_sql_table(
        table_name=f"us_{metric_name}_stats",
        con=db.connection(),
        index_col="metric"
    )
    data = data.replace(to_replace=np.NaN, value=None)

    return data.to_dict()

def get_metric_metadata_from_db(
        metric_code: str,
        db: Session,
    ) -> dict[str, dict[str, str]]:
    """Get metric's metadata from database."""
    with db.connection() as conn:
        res = db.scalars(text(f"""
            SELECT * FROM us_metrics_metadata
            WHERE code = :metric_code"""
            ), {"metric_code": metric_code}
            )

    return res.to_dict()

def get_metric_all_info_from_db(
        metric_name: str,
        limit: int,
        db: Session
) -> dict[str, dict[str, dict[str, float | None]]]:
    """Get metric's data and statistics from database."""
    with db.connection() as conn:
        data = pd.read_sql_table(
            table_name=f"us_{metric_name}_data",
            con=conn,
            index_col="date",
        )[-limit:]
        data = data.replace(to_replace=np.NaN, value=None)
        stats = pd.read_sql_table(
            table_name=f"us_{metric_name}_stats",
            con=conn,
            index_col="metric"
        )
    result = {"data": data.to_dict()}
    result.update({"statistics": stats.to_dict()})
    
    return result 