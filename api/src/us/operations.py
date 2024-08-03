import os
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from libs import exceptions


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
            table_name=f"us_{metric_code}_data",
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
            table_name=f"us_{metric_code}_stats",
            con=db.connection(),
            index_col="index"
        )
    except ValueError:
        raise exceptions.NoTableFoundException

    data = data.replace(to_replace=np.NaN, value=None)

    return data.to_dict()


def get_metric_metadata_from_db(
        metric_code: str,
        db: Session,
    ) -> dict[str, str]:
    """Get all metrics' metadata from database"""
    try:
        table = pd.read_sql_table(
            "us_metrics_metadata",
            con=db.connection(),
            index_col='code'
        ).loc[metric_code].to_dict()
        table.update({"code": metric_code})
        return table
    except Exception:
        raise exceptions.NoTableFoundException
    

def add_metric_endpoint_url_to_metadata(
        metadata: dict[str, str],
        base_api_url: str,
        ) -> dict[str, str]:
    """Add endpoint url to metric's metadata""" 
    metadata["url"] = os.path.join(
        base_api_url, "us/metric", metadata.get("code"), "metadata",
        )

    return metadata


def get_metric_all_info_from_db(
        metric_code: str,
        limit: Optional[int],
        base_api_url: str,
        db: Session
) -> dict[str, dict[str, str] | dict[str, dict[str, float | None]]]:
    """Get metric's data and statistics from database"""
    data = get_metric_data_from_db(metric_code, limit, db)
    stats = get_metric_statistics_from_db(metric_code, db)
    metadata = get_metric_metadata_from_db(metric_code, db)
    metadata = add_metric_endpoint_url_to_metadata(metadata, base_api_url)

    metric_info = {"metadata": metadata}
    metric_info.update({"data": data})
    metric_info.update({"statistics": stats})
    
    return metric_info


def create_endpoints_to_metrics_data(
        db: Session,
        base_api_url: str,
        ) -> dict[str, dict[str, str]]:
    """
    Create dictionary with base links to request data of available us metrics.
    End points names are derived from tables names in database.
    """
    try:
        with db.connection() as conn:
            metrics = pd.read_sql_table(
                table_name="us_metrics_metadata",
                con=conn,
                index_col="code",
            )
    except ValueError:
        raise exceptions.NoTableFoundException

    metrics = metrics.transpose().to_dict()

    for metric_code, metadata in metrics.items():
        metadata["code"] = metric_code
        metadata["url"] = os.path.join(base_api_url, "us/metric", metric_code)
        metadata["url_metadata"] = os.path.join(metadata.get("url"), "metadata")
        metadata["url_data"] = os.path.join(metadata.get("url"), "data")
        metadata["url_stats"] = os.path.join(metadata.get("url"), "stats")
        metrics.update({metric_code: metadata})
  
    return metrics