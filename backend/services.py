import os
import uuid

from fastapi import HTTPException, UploadFile, status
from models import Follow, Like, Media, Tweet, TweetMedia, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from utils.auth import generate_api_key

UPLOAD_DIR = "../frontend/app/media"


async def create_tweet_service(tweet_data, current_user, db: AsyncSession) -> Tweet:
    tweet = Tweet(content=tweet_data.tweet_data, author_id=current_user.id)
    db.add(tweet)
    await db.flush()

    if tweet_data.tweet_media_ids:
        media_result = await db.execute(
            select(Media).where(Media.id.in_(tweet_data.tweet_media_ids))
        )
        media_objects = media_result.scalars().all()
        found_media_ids = {media.id for media in media_objects}
        requested_media_ids = set(tweet_data.tweet_media_ids)
        missing_media_ids = requested_media_ids - found_media_ids

        if missing_media_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Media not found: {missing_media_ids}",
            )

        for media_id in tweet_data.tweet_media_ids:
            tweet_media = TweetMedia(tweet_id=tweet.id, media_id=media_id)
            db.add(tweet_media)

    await db.commit()
    await db.refresh(tweet, attribute_names=["tweet_media"])
    return tweet


async def save_media_service(file: UploadFile, db: AsyncSession) -> Media:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Filename is missing"
        )

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    content = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    media = Media(file_path=file_path)
    db.add(media)
    await db.commit()
    await db.refresh(media)
    return media


async def delete_tweet_service(tweet_id: int, current_user, db: AsyncSession) -> None:
    result = await db.execute(
        select(Tweet)
        .options(selectinload(Tweet.tweet_media))
        .where(Tweet.id == tweet_id)
    )
    tweet = result.scalar_one_or_none()

    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
        )

    if tweet.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can delete only your own tweets",
        )

    await db.delete(tweet)
    await db.commit()


async def like_tweet_service(db, user_id: int, tweet_id: int):
    tweet = await db.get(Tweet, tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    like = Like(user_id=user_id, tweet_id=tweet_id)
    db.add(like)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Already liked")


async def unlike_tweet_service(db, user_id: int, tweet_id: int):
    result = await db.execute(
        select(Like).where(Like.user_id == user_id, Like.tweet_id == tweet_id)
    )

    like = result.scalar_one_or_none()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    await db.delete(like)
    await db.commit()


async def follow_user_service(db, follower_id: int, following_id: int):
    if follower_id == following_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    user = await db.get(User, following_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    follow = Follow(follower_id=follower_id, following_id=following_id)
    db.add(follow)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Already following")


async def unfollow_user_service(db, follower_id: int, following_id: int):
    result = await db.execute(
        select(Follow).where(
            Follow.follower_id == follower_id, Follow.following_id == following_id
        )
    )
    follow = result.scalar_one_or_none()

    if not follow:
        raise HTTPException(status_code=404, detail="Follow not found")

    await db.delete(follow)
    await db.commit()


async def get_user_profile_service(db, user_id: int):
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    followers_result = await db.execute(
        select(Follow).where(Follow.following_id == user_id)
    )

    following_result = await db.execute(
        select(Follow).where(Follow.follower_id == user_id)
    )

    followers = followers_result.scalars().all()
    following = following_result.scalars().all()

    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [
                {"id": f.follower_id, "name": (await db.get(User, f.follower_id)).name}
                for f in followers
            ],
            "following": [
                {
                    "id": f.following_id,
                    "name": (await db.get(User, f.following_id)).name,
                }
                for f in following
            ],
        },
    }


async def get_feed_service(db, user_id: int):
    result = await db.execute(
        select(Follow.following_id).where(Follow.follower_id == user_id)
    )

    following_ids = [row[0] for row in result.all()]

    if not following_ids:
        return {"result": True, "tweets": []}

    tweets_result = await db.execute(
        select(Tweet)
        .where(Tweet.author_id.in_(following_ids))
        .options(
            selectinload(Tweet.likes),
            selectinload(Tweet.tweet_media).selectinload(TweetMedia.media),
            selectinload(Tweet.author),
        )
    )

    tweets = tweets_result.scalars().all()

    def build_tweet(tweet):
        return {
            "id": tweet.id,
            "content": tweet.content,
            "attachments": [tm.media.file_path for tm in tweet.tweet_media],
            "author": {
                "id": tweet.author.id,
                "name": tweet.author.name,
            },
            "likes": [
                {"user_id": like.user_id, "name": like.user.name if like.user else None}
                for like in tweet.likes
            ],
        }

    tweets_sorted = sorted(tweets, key=lambda t: len(t.likes), reverse=True)
    return {"result": True, "tweets": [build_tweet(t) for t in tweets_sorted]}


async def create_user_service(db: AsyncSession, name: str):
    api_key = generate_api_key()

    user = User(name=name, api_key=api_key)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def login_user_service(db: AsyncSession, api_key: str):
    result = await db.execute(select(User).where(User.api_key == api_key))

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return user
