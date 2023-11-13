import os
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np

BASE_API_URL = os.getenv("BASE_API_URL")


def get_metric_data_from_db(
        metric_code: str,
        limit: int,
        db: Session
    ) -> dict[str, dict[str, float | None]]:
    """
    Get metric's data from database (all constituents).
    """
    data = pd.read_sql_table(
        table_name=f"us_{metric_code}_data",
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
        table_name=f"us_{metric_code}_stats",
        con=db.connection(),
        index_col="metric"
    )
    data = data.replace(to_replace=np.NaN, value=None)

    return data.to_dict()


def get_metric_metadata_from_db(
        metric_code: str,
        db: Session,
    ) -> dict[str, str]:
    """Get all metrics' metadata from database."""
    columns = db.scalars(
        text(f"""
             SELECT column_name
             FROM information_schema.columns
             WHERE table_name = :table_name
             """), {"table_name": "us_metrics_metadata"}).all()
    data = db.execute(
        text(f"""
             SELECT * FROM us_metrics_metadata
             WHERE code = :metric_code
             """), {"metric_code": metric_code}).all()
    
    return {col: value for col, value in zip(columns, *data)}
    

def add_metric_endpoint_url_to_metadata(
        metadata: dict[str, str],
        base_api_url: str,
        ) -> dict[str, str]:
    """Add endpoint url to metric's metadata.""" 
    metadata["url"] = os.path.join(
        base_api_url, "us/metric", metadata.get("code"), "metadata",
        )

    return metadata


def get_metric_all_info_from_db(
        metric_code: str,
        limit: int,
        db: Session
) -> dict[str, dict[str, str] | dict[str, dict[str, float | None]]]:
    """Get metric's data and statistics from database."""
    with db.connection() as conn:
        data = get_metric_data_from_db(metric_code, limit, db)
        stats = get_metric_statistics_from_db(metric_code, db)
        metadata = get_metric_metadata_from_db(metric_code, db)
    
    metadata = add_metric_endpoint_url_to_metadata(metadata, BASE_API_URL)

    result = {"metadata": metadata}
    result.update({"data": data})
    result.update({"statistics": stats})
    
    return result 


def create_endpoints_to_metrics_data(
        db: Session,
        base_api_url: str = BASE_API_URL,
        ) -> dict[str, dict[str, str]]:
    """
    Create dictionary with base links to request data of available us metrics.
    End points names are derived from tables names in database.
    """
    with db.connection() as conn:
        metrics = pd.read_sql_table(
            table_name="us_metrics_metadata",
            con=conn,
            index_col="code",
        ).transpose().to_dict()

        for metric_code, metadata in metrics.items():
            metadata["url"] = os.path.join(base_api_url, "us/metric", metric_code)
            metadata["url_metadata"] = os.path.join(metadata.get("url"), "metadata")
            metadata["url_data"] = os.path.join(metadata.get("url"), "data")
            metadata["url_stats"] = os.path.join(metadata.get("url"), "stats")
            metrics.update({metric_code: metadata})
  
    return metrics