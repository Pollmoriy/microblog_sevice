from backend import models
from backend.database import get_db
from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user(
    api_key: str = Header(..., alias="api-key"), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.User).where(models.User.api_key == api_key))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return user
