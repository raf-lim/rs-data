from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.base import get_db
from operations import us


router_us = APIRouter(prefix="/us", tags=["us"])


@router_us.get("/metrics")
async def get_metrics_data_endpoints(db = Depends(get_db)) -> dict[str, str]:
    return us.create_endpoints_to_metrics_data(db)


@router_us.get("/metric/{metric}")
async def get_metric_data(
    metric: str, limit: int = 0, db: Session = Depends(get_db)
    ) -> dict[str, dict[str, float | None]]:
    
    return us.get_metric_data_from_db(metric, limit, db)


@router_us.get("/metric/{metric}/stats")
async def get_metric_statistics(
    metric: str, db: Session = Depends(get_db),
    ) -> dict[str, dict[str, float | None]]:
    
    return us.get_metric_statistics_from_db(metric, db)


@router_us.get("/metric/{metric}/all")
async def get_metric_data_and_statistics(
    metric: str, limit: int = 0, db: Session = Depends(get_db),
    ) -> dict[str, dict[str, dict[str, float | None]]]:
    
    return us.get_metric_all_info_from_db(metric, limit, db)