from os import getenv
from fastapi import FastAPI
import uvicorn
from routers.us import router_us


app = FastAPI()
app.include_router(router_us)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(getenv("PORT", default=5000)))