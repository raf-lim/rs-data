from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.base import get_db
from operations import eu


router_eu = APIRouter(prefix="/eu", tags=["eu"])


LIMIT = 12

@router_eu.get("/metrics")
async def get_metrics_metadata(
    db: Session = Depends(get_db),
    ) -> dict[str, dict[str, str]]:
    return eu.create_all_metrics_metadata(db)


@router_eu.get("/metric/{metric_code}")
async def get_metric_all_data(
    metric_code: str, limit: int = LIMIT, db: Session = Depends(get_db),
    ) -> dict[str, dict[str, str] | dict[str, dict[str, float | None]]]:
    
    return eu.get_metric_all_info(metric_code, limit, db)


@router_eu.get("/metric/{metric_code}/metadata")
async def get_metric_metadata(metric_code) -> dict[str, str]:
    
    return eu.create_metric_metadata(metric_code)


@router_eu.get("/metric/{metric_code}/data")
async def get_metric_data(
    metric_code: str, limit: int = LIMIT , db: Session = Depends(get_db)
    ) -> dict[str, dict[str, float | None]]:
    
    return eu.get_metric_data_from_db(metric_code, limit, db)


@router_eu.get("/metric/{metric_code}/stats")
async def get_metric_statistics(
    metric_code: str, db: Session = Depends(get_db),
    ) -> dict[str, dict[str, float | None]]:
    
    return eu.get_metric_statistics_from_db(metric_code, db)


@router_eu.get("/countries")
async def get_countries_codes(
    db: Session = Depends(get_db)
    ) -> list[str]:
    
    return eu.extract_countries_codes_from_db(db)


@router_eu.get("/country/{country_code}/data")
async def get_country_data(
    country_code: str, limit: int = LIMIT, db: Session = Depends(get_db)
    ) -> dict[str, dict[str, float | None]]:
    
    return eu.get_country_data_from_db(country_code, limit, db)


@router_eu.get("/country/{country_code}/stats")
async def get_country_statistics(
    country_code: str, db: Session = Depends(get_db),
    ) -> dict[str, dict[str, float | None]]:
    
    return eu.get_country_statistics_from_db(country_code, db)
