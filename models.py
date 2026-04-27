from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine, func
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy import DateTime

class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    content = Column(String(800), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('User', back_populates='tweets')
    likes = relationship('Like', back_populates='tweet', cascade="all, delete")
    media = relationship('Media', back_populates='tweet', cascade="all, delete")



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    api_key = Column(String(100), nullable=False, unique=True)

    tweets = relationship('Tweet', back_populates='author', cascade="all, delete")
    likes = relationship('Like', back_populates='user', cascade="all, delete")



class Like(Base):
    __tablename__ = 'likes'
    __table_args__ = (UniqueConstraint('user_id', 'tweet_id'),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tweet_id = Column(Integer, ForeignKey('tweets.id'))

    user = relationship('User', back_populates='likes')
    tweet = relationship('Tweet', back_populates='likes')


class Follow(Base):
    __tablename__ = 'followers'
    __table_args__ = (UniqueConstraint('follower_id', 'following_id'),)

    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('users.id'))
    following_id = Column(Integer, ForeignKey('users.id'))


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    file_path = Column(String(200), nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweets.id'))

    tweet = relationship('Tweet', back_populates='media')
