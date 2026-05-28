from database import get_db
from dependencies import get_current_user
from fastapi import APIRouter, Depends, File, UploadFile, status
from schemas import (MediaResponse, TweetCreate, TweetResponse,
                     UserCreate, UserResponse)
from services import (create_tweet_service, create_user_service,
                      delete_tweet_service, follow_user_service,
                      get_feed_service, get_user_profile_service,
                      like_tweet_service,
                      save_media_service, unfollow_user_service,
                      unlike_tweet_service)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api", tags=["API"])


@router.post(
    "/tweets", response_model=TweetResponse, status_code=status.HTTP_201_CREATED
)
async def create_tweet(
    tweet_data: TweetCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    tweet = await create_tweet_service(
        tweet_data=tweet_data, current_user=current_user, db=db
    )
    return TweetResponse(tweet_id=tweet.id)


@router.delete("/tweets/{tweet_id}")
async def delete_tweet(
    tweet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    await delete_tweet_service(
        tweet_id=tweet_id,
        current_user=current_user,  # ✔ исправлено (латинская c)
        db=db,
    )
    return {"result": True}


@router.get("/tweets")
async def get_feed(
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    return await get_feed_service(db, current_user.id)


@router.post(
    "/medias", response_model=MediaResponse, status_code=status.HTTP_201_CREATED
)
async def upload_media(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    media = await save_media_service(file=file, db=db)
    return MediaResponse(media_id=media.id)


@router.post("/tweets/{tweet_id}/likes")
async def like_tweet(
    tweet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    await like_tweet_service(db, current_user.id, tweet_id)
    return {"result": True}


@router.delete("/tweets/{tweet_id}/likes")
async def unlike_tweet(
    tweet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    await unlike_tweet_service(db, current_user.id, tweet_id)
    return {"result": True}


@router.post("/users/{user_id}/follow")
async def follow_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    await follow_user_service(db, current_user.id, user_id)
    return {"result": True}


@router.delete("/users/{user_id}/follow")
async def unfollow_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    await unfollow_user_service(db, current_user.id, user_id)
    return {"result": True}


@router.get("/users/me")
async def get_me(
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    return await get_user_profile_service(db, current_user.id)


@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await get_user_profile_service(db, user_id)


@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await create_user_service(db, user.name)

    return UserResponse(id=new_user.id, name=new_user.name, api_key=new_user.api_key)
