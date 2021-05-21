from sqlalchemy import create_engine
from src.twitteralchemy.models import pydantic as schemas, orm as models


def create_tables(connection_string: str):
    # create tables
    engine = create_engine(connection_string, echo=True)
    models.Base.metadata.create_all(engine)


def get_tweet_model(tweet: schemas.Tweet) -> models.Tweet:
    """
    Map from the tweet schema object to the tweet orm object for
    database insertion.
    """
    db_tweet = models.Tweet(
        id=tweet.id,
        text=tweet.text,
        author_id=tweet.author_id,
        conversation_id=tweet.conversation_id,
        created_at=tweet.created_at,
        in_reply_to_user_id=tweet.in_reply_to_user_id,
        lang=tweet.lang,
        public_metrics_retweet_count=tweet.public_metrics.retweet_count,
        public_metrics_reply_count=tweet.public_metrics.reply_count,
        public_metrics_like_count=tweet.public_metrics.like_count,
        public_metrics_quote_count=tweet.public_metrics.quote_count,
        possibly_sensitive=tweet.possibly_sensitive,
        reply_settings=tweet.reply_settings,
        source=tweet.source
    )

    # assign referenced users
    db_tweet.referenced_tweets = [
        models.ReferencedTweet(
            tweet_id=tweet.id,
            id=ref.id,
            type=ref.type
        ) for ref in tweet.referenced_tweets
    ]

    return db_tweet


def get_user_model(user: schemas.User) -> models.User:
    """
    Map from the user schema object to the user orm object for
    database insertion.
    """
    db_user = models.User(
        id=user.id,
        name=user.name,
        username=user.username,
        created_at=user.created_at,
        description=user.description,
        location=user.location,
        pinned_tweet_id=user.pinned_tweet_id,
        profile_image_url=user.profile_image_url,
        protected=user.protected,
        public_metrics_followers_count=user.public_metrics.follower_count,
        public_metrics_following_count=user.public_metrics.following_count,
        public_metrics_tweet_count=user.public_metrics.tweet_count,
        public_metrics_listed_count=user.public_metrics.listed_count,
        url=user.url,
        verified=user.verified
    )

    return db_user
