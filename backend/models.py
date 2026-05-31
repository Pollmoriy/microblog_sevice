from backend.database import Base
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint, func)
from sqlalchemy.orm import relationship


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    content = Column(String(800), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="tweets")
    likes = relationship("Like", back_populates="tweet", cascade="all, delete")
    tweet_media = relationship(
        "TweetMedia", back_populates="tweet", cascade="all, delete-orphan"
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    api_key = Column(String(100), nullable=False, unique=True)

    tweets = relationship("Tweet", back_populates="author", cascade="all, delete")
    likes = relationship("Like", back_populates="user", cascade="all, delete")
    followers = relationship(
        "Follow", foreign_keys="Follow.following_id", back_populates="following"
    )
    following = relationship(
        "Follow", foreign_keys="Follow.follower_id", back_populates="follower"
    )


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("user_id", "tweet_id"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=False)

    user = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")


class Follow(Base):
    __tablename__ = "follows"
    __table_args__ = (UniqueConstraint("follower_id", "following_id"),)

    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    following = relationship(
        "User", foreign_keys=[following_id], back_populates="followers"
    )
    follower = relationship(
        "User", foreign_keys=[follower_id], back_populates="following"
    )


class TweetMedia(Base):
    __tablename__ = "tweet_media"
    __table_args__ = (UniqueConstraint("tweet_id", "media_id"),)

    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=False)
    media_id = Column(Integer, ForeignKey("media.id"), nullable=False)

    tweet = relationship("Tweet", back_populates="tweet_media")
    media = relationship("Media", back_populates="tweet_media")


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    file_path = Column(String(200), nullable=False)

    tweet_media = relationship("TweetMedia", back_populates="media")
