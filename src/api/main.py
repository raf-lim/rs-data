from fastapi import FastAPI
from routers.us import router_us

app = FastAPI()
app.include_router(router_us)