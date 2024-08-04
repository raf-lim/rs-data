from os import getenv
from fastapi import FastAPI
import uvicorn
from us.routers import router_us
from eu.routers import router_eu
from dbmf.routers import router_dbmf


app = FastAPI()
app.include_router(router_us)
app.include_router(router_eu)
app.include_router(router_dbmf)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(getenv("PORT", default=5000)))