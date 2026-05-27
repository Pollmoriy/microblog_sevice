import os
import uuid

from fastapi import UploadFile, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Media, Tweet, TweetMedia

UPLOAD_DIR = "app/media"


async def create_tweet_service(tweet_data, current_user, db: AsyncSession) -> Tweet:
    tweet = Tweet(content=tweet_data.tweet_data, author_id=current_user.id)
    db.add(tweet)
    await db.flush()

    if tweet_data.tweet_media_ids:
        media_result = await db.execute(select(Media).where(Media.id.in_(tweet_data.tweet_media_ids)))
        media_objects = media_result.scalars().all()
        found_media_ids = {media.id for media in media_objects}
        requested_media_ids = set(tweet_data.tweet_media_ids)
        missing_media_ids = requested_media_ids - found_media_ids

        if missing_media_ids:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Media not found: {missing_media_ids}")

        for media_id in tweet_data.tweet_media_ids:
            tweet_media = TweetMedia(tweet_id=tweet.id, media_id=media_id)
            db.add(tweet_media)

    await db.commit()
    await db.refresh(tweet, attribute_names=["tweet_media"])
    return tweet


async def save_media_service(file: UploadFile, db: AsyncSession) -> Media:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename is missing")

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
    result = await db.execute(select(Tweet).options(selectinload(Tweet.tweet_media)).where(Tweet.id == tweet_id))
    tweet = result.scalar_one_or_none()

    if not tweet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found")

    if tweet.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete only your own tweets")

    await db.delete(tweet)
    await db.commit()