from fastapi import FastAPI

import models

from database import engine
from routers import router


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


app.include_router(router)
