import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from twitteralchemy import Tweet

# load test tweet data
with open("tweet.json", 'r') as f:
    response = json.load(f)
tweets = response['data']

# validate tweet objects
tweets = [Tweet(**tw) for tw in tweets]
print(tweets)

# convert to orm objects
tweets_orm = [tw.to_orm() for tw in tweets]
print(tweets_orm)

# create session and add objects
engine = create_engine(os.environ['DB_CONNECTION_STRING'], echo=True)
with Session(engine) as session:
    session.add_all(tweets_orm)
    session.commit()


