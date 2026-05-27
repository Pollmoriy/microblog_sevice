from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependencies import get_current_user
from schemas import TweetCreate, TweetResponse, MediaResponse
from services import save_media_service, create_tweet_service, delete_tweet_service

router = APIRouter(tags=["API"])

@router.post("/api/tweets", response_model=TweetResponse, status_code=status.HTTP_201_CREATED)
async def create_tweet(
    tweet_data: TweetCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)):
    tweet = await create_tweet_service(
        tweet_data=tweet_data,
        current_user=current_user,
        db=db,
    )

    return TweetResponse(
        tweet_id=tweet.id,
    )

@router.post(
    "/api/medias",
    response_model=MediaResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_media(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)):
    media = await save_media_service(
        file=file,
        db=db,
    )

    return MediaResponse(
        media_id=media.id,
    )

@router.delete("/api/tweets/{tweet_id}")
async def delete_tweet(
    tweet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)):
    await delete_tweet_service(
        tweet_id=tweet_id,
        current_user=current_user,
        db=db,
    )

    return {"result": True}
