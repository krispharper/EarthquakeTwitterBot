import os
import requests
import tweepy
from datetime import datetime,timedelta

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

print(consumer_key)
print(consumer_secret)
print(access_token)
print(access_token_secret)

print(1)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
print(2)
auth.set_access_token(access_token, access_token_secret)
print(3)
twitter = tweepy.API(auth)
print(4)

print(twitter.home_timeline()[0])

try:
    start_time = datetime.utcnow() - timedelta(hours=1)
    #usgs_url = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={0}&minmagnitude=5".format(start_time.isoformat())
    usgs_url = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={0}".format(start_time.isoformat())

    response = requests.get(usgs_url)
    earthquakes = response.json()['features']

    for earthquake in [e['properties'] for e in earthquakes]:
        tweet_text = "{0}\n{1}".format(earthquake['title'], earthquake['detail'])
        print(tweet_text)
        twitter.update_status(tweet_text)

except Exception as e:
    print("Error ocurred")
    print(e)
