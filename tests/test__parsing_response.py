import json
from twitteralchemy import Tweet, Includes

# load test tweet data
with open("tweet.json", 'r') as f:
    response = json.load(f)
tweets = response['data']
includes = response['includes']

# validate tweet objects
tweets = [Tweet(**tw) for tw in tweets]
print(tweets)

# convert to orm objects
tweets_dict = [tw.to_dict() for tw in tweets]
print(tweets_dict)

# validate Includes objects
includes = Includes(**includes)

# convert to dict objects
includes_dict = includes.to_dict()
print(includes_dict)