from os import getenv
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import get_db
from operations import us
from libs import exceptions

router_us = APIRouter(prefix="/us", tags=["us"])

LIMIT = int(getenv("US_LIMIT_MONTHS"))


@router_us.get("/metrics")
async def get_metrics_data_endpoints(
    db: Session = Depends(get_db),
    ) -> dict[str, dict[str, str]]:
    try:
        return us.create_endpoints_to_metrics_data(db)
    except exceptions.TableNoFoundException:
        raise HTTPException(status_code=404)


@router_us.get("/metric/{metric_code}")
async def get_metric_all_data(
    metric_code: str, limit: int = LIMIT, db: Session = Depends(get_db),
    ) -> dict[str, dict[str, str] | dict[str, dict[str, float | None]]]:
    try:
        return us.get_metric_all_info_from_db(metric_code, limit, db)
    except exceptions.TableNoFoundException:
        raise HTTPException(status_code=404)


@router_us.get("/metric/{metric_code}/metadata")
async def get_metric_metadata(
    metric_code,
    db: Session = Depends(get_db),
    ) -> dict[str, Any]:
    try:
        metadata = us.get_metric_metadata_from_db(metric_code, db)
        return us.add_metric_endpoint_url_to_metadata(metadata)
    except exceptions.TableNoFoundException:
        raise HTTPException(status_code=404)


@router_us.get("/metric/{metric_code}/data")
async def get_metric_data(
    metric_code: str, limit: int = LIMIT, db: Session = Depends(get_db)
    ) -> dict[str, dict[str, float | None]]:
    try:
        return us.get_metric_data_from_db(metric_code, limit, db)
    except exceptions.TableNoFoundException:
        raise HTTPException(status_code=404) 


@router_us.get("/metric/{metric_code}/stats")
async def get_metric_statistics(
    metric_code: str, db: Session = Depends(get_db),
    ) -> dict[str, dict[str, float | None]]:
    try:
        return us.get_metric_statistics_from_db(metric_code, db)
    except exceptions.TableNoFoundException:
        raise HTTPException(status_code=404) 
