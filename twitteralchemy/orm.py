import os
from sqlalchemy import create_engine, ForeignKey, Column, DateTime, Text, Boolean, Integer, BigInteger
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()


# See: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweets
class Tweet(Base):
    __tablename__ = os.environ.get('DB_TABLE_TWEET', 'tweet')
    id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    text = Column(Text)
    author_id = Column(BigInteger)
    conversation_id = Column(BigInteger)
    created_at = Column(DateTime)
    in_reply_to_user_id = Column(BigInteger)
    lang = Column(Text)
    public_metrics_retweet_count = Column(Integer)
    public_metrics_reply_count = Column(Integer)
    public_metrics_like_count = Column(Integer)
    public_metrics_quote_count = Column(Integer)
    possibly_sensitive = Column(Boolean)
    reply_settings = Column(Text)
    source = Column(Text)

    referenced_tweets = relationship('ReferencedTweet', backref=__tablename__)

    def __repr__(self):
        nchars = 50
        txt = self.text if len(self.text) <= nchars else self.text[:nchars] + '...'
        return f"<id={self.id} tweet_text='{txt}'>"


class ReferencedTweet(Base):
    __tablename__ = os.environ.get('DB_TABLE_REFERENCED_TWEET', 'referenced_tweet')
    uid = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    tweet_id = Column(ForeignKey(f'{Tweet.__tablename__}.id'), nullable=False)
    id = Column(BigInteger)
    type = Column(Text)


# See: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user
class User(Base):
    __tablename__ = os.environ.get('DB_TABLE_USER', 'user')
    id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    name = Column(Text)
    username = Column(Text)
    created_at = Column(DateTime)
    description = Column(Text)
    location = Column(Text)
    pinned_tweet_id = Column(BigInteger)
    profile_image_url = Column(Text)
    protected = Column(Boolean)
    public_metrics_followers_count = Column(Integer)
    public_metrics_following_count = Column(Integer)
    public_metrics_tweet_count = Column(Integer)
    public_metrics_listed_count = Column(Integer)
    url = Column(Text)
    verified = Column(Boolean)

    def __repr__(self):
        return f"<id={self.id} username={self.username} name={self.name}>"


def create_tables(connection_string: str):
    # create tables
    engine = create_engine(connection_string, echo=True)
    Base.metadata.create_all(engine)
