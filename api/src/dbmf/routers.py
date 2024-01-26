from typing import Iterable
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import get_db
from . import operations
from libs import exceptions

router_dbmf = APIRouter(prefix="/dbmf", tags=["DBMF"])


@router_dbmf.get("/tickers")
async def get_dbmf_tickers(
    db: Session = Depends(get_db)
    ) -> dict[str, dict[str, str]]:
    try:
        return operations.extract_tickers_from_db(db)
    except exceptions.NoTableFoundException:
        raise HTTPException(
            status_code=404,
            detail="Tickers' table not found"
        )
    except exceptions.NoDbmfTickerFoundException:
        raise HTTPException(
            status_code=200,
            detail="Tickers' table empty"
        )
    

@router_dbmf.get("/ticker/{ticker}")
async def get_stats(
    ticker: str, db: Session = Depends(get_db)
    ) -> dict[str, dict[str, float | None]]:
    try:
        return operations.get_position_stats(ticker, db)
    except exceptions.NoTableFoundException:
        raise HTTPException(
            status_code=404,
            detail=f"No {ticker.upper()} postion status table found"
        )