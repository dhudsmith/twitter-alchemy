import json
import abc
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum
import twitteralchemy.orm as orm


# --- Abstract Base ---

class TwitterAPIObject(BaseModel):

    @abc.abstractmethod
    def to_dict(self) -> dict:
        pass

    @abc.abstractmethod
    def to_full_dict(self) -> dict:
        pass


# --- Referenced Tweet Schemas ---
class ReferencedTweetType(Enum):
    RETWEETED = 'retweeted'
    QUOTED = 'quoted'
    REPLIED_TO = 'replied_to'


class ReferencedTweet(BaseModel):
    id: int
    type: ReferencedTweetType

    class Config:
        use_enum_values = True
        extra = 'forbid'


# --- User Schemas ---

class UserPublicMetrics(BaseModel):
    followers_count: int = None
    following_count: int = None
    tweet_count: int = None
    listed_count: int = None


class User(BaseModel):
    id: int
    name: str
    username: str
    created_at: Optional[datetime] = None
    protected: Optional[bool] = None
    location: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    verified: Optional[bool] = None
    public_metrics: Optional[UserPublicMetrics] = UserPublicMetrics()
    pinned_tweet_id: Optional[int] = None
    profile_image_url: Optional[str] = None

    entities: Optional[dict] = None  # Contents not automatically parsed
    withheld: Optional[dict] = None  # Contents not parsed automatically

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
            public_metrics_followers_count=self.public_metrics.followers_count,
            public_metrics_following_count=self.public_metrics.following_count,
            public_metrics_tweet_count=self.public_metrics.tweet_count,
            public_metrics_listed_count=self.public_metrics.listed_count,
            url=self.url,
            verified=self.verified
        )

        return orm_user

    def to_dict(self) -> dict:
        """
            Map from the User schema object to a python dict object
        """

        dict_user = dict(
            id=self.id,
            name=self.name,
            username=self.username,
            created_at=self.created_at,
            description=self.description,
            location=self.location,
            pinned_tweet_id=self.pinned_tweet_id,
            profile_image_url=self.profile_image_url,
            protected=self.protected,
            public_metrics_followers_count=self.public_metrics.followers_count,
            public_metrics_following_count=self.public_metrics.following_count,
            public_metrics_tweet_count=self.public_metrics.tweet_count,
            public_metrics_listed_count=self.public_metrics.listed_count,
            url=self.url,
            verified=self.verified
        )

        return dict_user

    def to_full_dict(self) -> dict:
        dict_buser = self.to_dict()

        dict_fuser = dict(
            entities=json.dumps(self.entities),
            withheld=json.dumps(self.withheld)
        )

        dict_buser.update(dict_fuser)

        return dict_buser


# --- Tweet Schemas ---

class Coordinates(BaseModel):
    # type: Optional[str] = None
    coordinates: Optional[str] = None  # Length 2

    class Config:
        extra = 'forbid'


class Geo(BaseModel):
    coordinates: Optional[Coordinates] = Coordinates()
    place_id: Optional[str] = None

    class Config:
        extra = 'forbid'


class TweetPublicMetrics(BaseModel):
    retweet_count: int = None
    reply_count: int = None
    like_count: int = None
    quote_count: int = None
    impression_count: int = None


class ReplySettings(Enum):
    EVERYONE = 'everyone'
    MENTIONED_USERS = 'mentionedUsers'
    FOLLOWING = 'following'


class Tweet(BaseModel):
    id: int
    text: Optional[str] = None
    created_at: Optional[datetime] = None
    author_id: Optional[int] = None
    conversation_id: Optional[int] = None
    in_reply_to_user_id: Optional[int] = None
    referenced_tweets: Optional[List[ReferencedTweet]] = []
    public_metrics: Optional[TweetPublicMetrics] = TweetPublicMetrics()
    possibly_sensitive: Optional[bool] = None
    lang: Optional[str] = None
    reply_settings: Optional[ReplySettings] = None
    source: Optional[str] = None

    # Extra attributes included in to_full_dict
    attachments: Optional[dict]  # Contents not parsed automatically
    geo: Optional[Geo] = Geo()
    context_annotations: Optional[dict] = None  # Contents not parsed automatically
    entities: Optional[dict] = None  # Contents not parsed automatically
    withheld: Optional[dict] = None  # Contents not parsed automatically

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
            public_metrics_impression_count=self.public_metrics.impression_count,
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

    def to_dict(self) -> dict:
        """
        Map from the tweet schema object to a python dict object
        """
        dict_tweet = dict(
            id=str(self.id),
            text=self.text,
            author_id=str(self.author_id),
            conversation_id=str(self.conversation_id),
            created_at=self.created_at,
            in_reply_to_user_id=str(self.in_reply_to_user_id),
            lang=self.lang,
            public_metrics_retweet_count=self.public_metrics.retweet_count,
            public_metrics_reply_count=self.public_metrics.reply_count,
            public_metrics_like_count=self.public_metrics.like_count,
            public_metrics_quote_count=self.public_metrics.quote_count,
            public_metrics_impression_count=self.public_metrics.impression_count,
            possibly_sensitive=self.possibly_sensitive,
            reply_settings=self.reply_settings,
            source=self.source
        )

        return dict_tweet

    def to_full_dict(self) -> dict:
        """
        Map from the tweet schema object to a python dict object, including additional 
            attributes not in orm
        """
        dict_btweet = self.to_dict()

        dict_ftweet = dict(
            attachments=json.dumps(self.attachments),
            geo_place_id=self.geo.place_id,
            geo_coordinates=self.geo.coordinates.coordinates,
            context_annotations=json.dumps(self.context_annotations),
            entities=json.dumps(self.entities),
            withheld=json.dumps(self.withheld)
        )

        dict_btweet.update(dict_ftweet)

        return dict_btweet


# --- Media Schemas ---

class MediaType(Enum):
    ANIMATED_GIF = 'animated_gif'
    PHOTO = 'photo'
    VIDEO = 'video'


class Media(BaseModel):
    media_key: Optional[str] = None
    type: Optional[MediaType] = None
    url: Optional[str] = None
    duration_ms: Optional[int] = None
    height: Optional[int] = None
    width: Optional[int]
    preview_image_url: Optional[str] = None
    public_metrics: Optional[dict] = None
    alt_text: Optional[str] = None

    class Config:
        use_enum_values = True

    def to_dict(self) -> dict:
        """
        Map from the User schema object to a python dict object
        """

        dict_media = dict(
            media_key=self.media_key,
            type=self.type,
            url=self.url,
            duration_ms=self.duration_ms,
            height=self.height,
            width=self.width,
            preview_image_url=self.preview_image_url,
            public_metrics=json.dumps(self.public_metrics),
            alt_text=self.alt_text
        )

        return dict_media

    def to_full_dict(self) -> dict:
        """
        Placeholder for dividing information later, identical to to_dict method
        """

        return self.to_dict()


# --- Poll Schemas ---

class PollVotingStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"


class Poll(BaseModel):
    id: str
    options: Optional[List[dict]] = None
    duration_minutes: Optional[int] = None
    end_datetime: Optional[str] = None
    voting_status: Optional[PollVotingStatus] = None

    class Config:
        use_enum_values = True

    def to_dict(self):
        """
        Map from the Poll schema object to a python dict object
        """

        dict_poll = dict(
            id=self.id,
            options=json.dumps(self.options),
            duration_minutes=self.duration_minutes,
            end_datetime=self.end_datetime,
            voting_status=self.voting_status
        )

        return dict_poll

    def to_full_dict(self):
        """
        Placeholder for dividing information later, identical to to_dict method
        """
        return self.to_dict()


# --- Place Schemas ---

class Place(BaseModel):
    full_name: str
    id: str
    contained_within: List[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    geo: Optional[dict] = None
    name: Optional[str] = None
    place_type: Optional[str] = None  # TODO: get place types and create enum

    class Config:
        use_enum_values = True

    def to_dict(self):
        """
        Map from the Place shema object to a python dict object
        """

        dict_place = dict(
            full_name=self.full_name,
            id=self.id,
            contained_within=self.contained_within,
            country=self.country,
            country_code=self.country_code,
            geo=json.dumps(self.geo),
            name=self.name,
            place_type=self.place_type
        )

        return dict_place

    def to_full_dict(self):
        """
        Placeholder for dividing information later, identical to to_dict method
        """
        return self.to_dict()


# --- Includes Schema ---

class Includes(BaseModel):
    tweets: Optional[List[Tweet]] = None
    users: Optional[List[User]] = None
    places: Optional[List[Place]] = None
    media: Optional[List[Media]] = None
    polls: Optional[List[Poll]] = None

    def to_dict(self) -> dict:
        """
        Maps includes schema and all child object lists to python dictionaries
        """
        dict_inc = dict(
            tweets=[tw.to_dict() for tw in self.tweets] if self.tweets else None,
            users=[us.to_dict() for us in self.users] if self.users else None,
            places=[pl.to_dict() for pl in self.places] if self.places else None,
            media=[md.to_dict() for md in self.media] if self.media else None,
            polls=[po.to_dict() for po in self.polls] if self.polls else None
        )

        return dict_inc

    def to_full_dict(self) -> dict:
        """
        Map from the includes schema object and child objects to a python dict object, including additional 
            attributes not in orm
        """
        dict_inc = dict(
            tweets=[tw.to_full_dict() for tw in self.tweets] if self.tweets else None,
            users=[us.to_full_dict() for us in self.users] if self.users else None,
            places=[pl.to_full_dict() for pl in self.places] if self.places else None,
            media=[md.to_full_dict() for md in self.media] if self.media else None,
            polls=[po.to_full_dict() for po in self.polls] if self.polls else None
        )

        return dict_inc
