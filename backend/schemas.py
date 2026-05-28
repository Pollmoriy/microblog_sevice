from typing import Literal

from pydantic import BaseModel, Field


class TweetCreate(BaseModel):
    tweet_data: str = Field(min_length=1, max_length=800)
    tweet_media_ids: list[int] | None = None


class TweetResponse(BaseModel):
    result: Literal[True] = True
    tweet_id: int


class MediaResponse(BaseModel):
    result: Literal[True] = True
    media_id: int


class ErrorResponse(BaseModel):
    result: Literal[False] = False
    error_type: str
    error_message: str


class UserCreate(BaseModel):
    name: str


class UserResponse(BaseModel):
    id: int
    name: str
    api_key: str


class LoginRequest(BaseModel):
    api_key: str
