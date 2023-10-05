from fastapi import FastAPI, HTTPException, Depends
import pandas as pd

from apps.db.base import get_db

app = FastAPI()

@app.get("/")
async def root(db = Depends(get_db)):
    data = pd.read_sql_table(
        "housing_data",
        con=db.connection(),
        index_col="date"
        )
    
    return data.to_dict()
