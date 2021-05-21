from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum
import twitteralchemy.orm as orm


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

    def to_orm(self) -> orm.Tweet:
        """
        Map from the tweet schema object to the tweet orm object for
        database insertion.
        """
        orm_tweet = orm.Tweet(
            id=self.id,
            text=self.text,
            author_id=self.author_id,
            conversation_id=self.conversation_id,
            created_at=self.created_at,
            in_reply_to_user_id=self.in_reply_to_user_id,
            lang=self.lang,
            public_metrics_retweet_count=self.public_metrics.retweet_count,
            public_metrics_reply_count=self.public_metrics.reply_count,
            public_metrics_like_count=self.public_metrics.like_count,
            public_metrics_quote_count=self.public_metrics.quote_count,
            possibly_sensitive=self.possibly_sensitive,
            reply_settings=self.reply_settings,
            source=self.source
        )

        # assign referenced users
        orm_tweet.referenced_tweets = [
            orm.ReferencedTweet(
                tweet_id=self.id,
                id=ref.id,
                type=ref.type
            ) for ref in self.referenced_tweets
        ]

        return orm_tweet


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

    def to_orm(self) -> orm.User:
        orm_user = orm.User(
            id=self.id,
            name=self.name,
            username=self.username,
            created_at=self.created_at,
            description=self.description,
            location=self.location,
            pinned_tweet_id=self.pinned_tweet_id,
            profile_image_url=self.profile_image_url,
            protected=self.protected,
            public_metrics_followers_count=self.public_metrics.follower_count,
            public_metrics_following_count=self.public_metrics.following_count,
            public_metrics_tweet_count=self.public_metrics.tweet_count,
            public_metrics_listed_count=self.public_metrics.listed_count,
            url=self.url,
            verified=self.verified
        )

        return orm_user
