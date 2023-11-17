from os import getenv
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import get_db
from operations import eu
from libs import exceptions

router_eu = APIRouter(prefix="/eu", tags=["eu"])

LIMIT = int(getenv("EU_LIMIT_MONTHS"))


@router_eu.get("/metrics")
async def get_metrics_metadata(
    db: Session = Depends(get_db),
    ) -> dict[str, dict[str, str]]:
    try:
        return eu.create_all_metrics_metadata(db)
    except exceptions.NoEuMetricTableFound:
        raise HTTPException(
            status_code=404,
            detail="No metric's table found.")


@router_eu.get("/metric/{metric_code}")
async def get_metric_all_data(
    metric_code: str, limit: int = LIMIT, db: Session = Depends(get_db),
    ) -> dict[str, dict[str, str] | dict[str, dict[str, float | None]]]:
    try:
        return eu.get_metric_all_info(metric_code, limit, db)
    except exceptions.NoTableFoundException:
        raise HTTPException(status_code=404)


@router_eu.get("/metric/{metric_code}/metadata")
async def get_metric_metadata(metric_code) -> dict[str, str]:
    
    return eu.create_metric_metadata(metric_code)


@router_eu.get("/metric/{metric_code}/data")
async def get_metric_data(
    metric_code: str, limit: int = LIMIT , db: Session = Depends(get_db)
    ) -> dict[str, dict[str, float | None]]:
    try:
        return eu.get_metric_data_from_db(metric_code, limit, db)
    except exceptions.NoTableFoundException:
        raise HTTPException(status_code=404)


@router_eu.get("/metric/{metric_code}/stats")
async def get_metric_statistics(
    metric_code: str, db: Session = Depends(get_db),
    ) -> dict[str, dict[str, float | None]]:
    try:
        return eu.get_metric_statistics_from_db(metric_code, db)
    except exceptions.NoTableFoundException:
        raise HTTPException(status_code=404)


@router_eu.get("/countries")
async def get_countries_codes(
    db: Session = Depends(get_db)
    ) -> list[str]:
    try:
        return eu.extract_countries_codes_from_db(db)
    except exceptions.NoEuCountryTableFound:
        raise HTTPException(
            status_code=404,
            detail="No country's table found.",
            )


@router_eu.get("/country/{country_code}/data")
async def get_country_data(
    country_code: str, limit: int = LIMIT, db: Session = Depends(get_db)
    ) -> dict[str, dict[str, float | None]]:
    try:
        return eu.get_country_data_from_db(country_code, limit, db)
    except exceptions.NoTableFoundException:
        raise HTTPException(status_code=404)


@router_eu.get("/country/{country_code}/stats")
async def get_country_statistics(
    country_code: str, db: Session = Depends(get_db),
    ) -> dict[str, dict[str, float | None]]:
    try:
        return eu.get_country_statistics_from_db(country_code, db)
    except exceptions.NoTableFoundException:
        raise HTTPException(
            status_code=404,
            detail="No country's table found."
            )
