from typing import List

from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select
from sqlalchemy import desc
import models
import schemas
from database import engine, session

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()
