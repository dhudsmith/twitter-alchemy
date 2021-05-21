from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ReferencedTweetType(Enum):
    RETWEETED = 'retweeted'
    QUOTED = 'quoted'
    REPLIED_TO = 'replied_to'


class ReferencedTweet(BaseModel):
    id: str
    type: ReferencedTweetType

    class Config:
        use_enum_values = True
        extra = 'forbid'


class TweetPublicMetrics(BaseModel):
    retweet_count: int = None
    reply_count: int = None
    like_count: int = None
    quote_count: int = None

    class Config:
        extra = 'forbid'


class ReplySettings(Enum):
    EVERYONE = 'everyone'
    MENTIONED_USERS = 'mentionedUsers'
    FOLLOWING = 'following'


class Tweet(BaseModel):
    id: str
    text: Optional[str] = None
    created_at: Optional[datetime] = None
    author_id: Optional[str] = None
    conversation_id: Optional[str] = None
    in_reply_to_user_id: Optional[str] = None
    referenced_tweets: Optional[List[ReferencedTweet]] = []
    public_metrics: Optional[TweetPublicMetrics] = TweetPublicMetrics()
    possibly_sensitive: Optional[bool] = None
    lang: Optional[str] = None
    reply_settings: Optional[ReplySettings] = None
    source: Optional[str] = None

    class Config:
        use_enum_values = True


class UserPublicMetrics(BaseModel):
    follower_count: int = None
    following_count: int = None
    tweet_count: int = None
    listed_count: int = None

    class Config:
        extra = 'forbid'


class User(BaseModel):
    id: str
    name: str
    username: str
    created_at: Optional[datetime] = None
    protected: Optional[bool] = None
    location: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    verified: Optional[str] = None
    public_metrics: Optional[UserPublicMetrics] = UserPublicMetrics()
    pinned_tweet_id: Optional[int] = None
    profile_image_url: Optional[str] = None
