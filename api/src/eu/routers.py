from os import getenv
from typing import Iterable
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import get_db
from . import operations
from libs import exceptions
from libs.base_url import get_base_api_url

router_eu = APIRouter(prefix="/eu", tags=["Europe"])


@router_eu.get("/metrics")
async def get_metrics_metadata(
    base_api_url: str = Depends(get_base_api_url),
    db: Session = Depends(get_db),
) -> dict[str, dict[str, str]]:
    try:
        return operations.create_all_metrics_metadata(db, base_api_url)
    except exceptions.NoEuMetricTableFoundException:
        raise HTTPException(status_code=404, detail="No metric's table found.")


@router_eu.get("/metric/{metric_code}")
async def get_metric_all_data(
    metric_code: str,
    limit: int = 0,
    base_api_url=Depends(get_base_api_url),
    db: Session = Depends(get_db),
) -> dict[str, dict[str, str] | dict[str, dict[str, float | None]]]:
    try:
        return operations.get_metric_all_info(base_api_url, metric_code, limit, db)
    except exceptions.NoTableFoundException:
        raise HTTPException(status_code=404)


@router_eu.get("/metric/{metric_code}/metadata")
async def get_metric_metadata(
    metric_code: str, base_api_url=Depends(get_base_api_url)
) -> dict[str, str]:

    return operations.create_metric_metadata(metric_code, base_api_url)


@router_eu.get("/metric/{metric_code}/data")
async def get_metric_data(
    metric_code: str, limit: int = 0, db: Session = Depends(get_db)
) -> dict[str, dict[str, float | None]]:
    try:
        return operations.get_metric_data_from_db(metric_code, limit, db)
    except exceptions.NoTableFoundException:
        raise HTTPException(status_code=404)


@router_eu.get("/metric/{metric_code}/stats")
async def get_metric_statistics(
    metric_code: str,
    db: Session = Depends(get_db),
) -> dict[str, dict[str, float | None]]:
    try:
        return operations.get_metric_statistics_from_db(metric_code, db)
    except exceptions.NoTableFoundException:
        raise HTTPException(status_code=404)


@router_eu.get("/countries")
async def get_countries_codes(db: Session = Depends(get_db)) -> Iterable[str]:
    try:
        return operations.extract_countries_codes_from_db(db)
    except exceptions.NoEuCountryTableFoundException:
        raise HTTPException(
            status_code=404,
            detail="No country's table found.",
        )


@router_eu.get("/country/{country_code}/data")
async def get_country_data(
    country_code: str,
    limit: int = 0,
    db: Session = Depends(get_db),
) -> dict[str, dict[str, float | None]]:
    try:
        return operations.get_country_data_from_db(country_code, limit, db)
    except exceptions.NoTableFoundException:
        raise HTTPException(status_code=404)


@router_eu.get("/country/{country_code}/stats")
async def get_country_statistics(
    country_code: str,
    db: Session = Depends(get_db),
) -> dict[str, dict[str, float | None]]:
    try:
        return operations.get_country_statistics_from_db(country_code, db)
    except exceptions.NoEuMetricTableFoundException:
        raise HTTPException(status_code=404, detail="No metric's table found.")
    except exceptions.NoEuCountryTableFoundException:
        raise HTTPException(status_code=404, detail="No country's table found.")
