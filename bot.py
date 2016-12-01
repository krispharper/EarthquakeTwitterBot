import os
import requests
import tweepy
from datetime import datetime,timedelta
import time

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter = tweepy.API(auth)
start_time = datetime.utcnow() - timedelta(hours=1)

try:
    while True:
        usgs_url = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={0}".format(start_time.isoformat())
        response = requests.get(usgs_url)
        earthquakes = response.json()['features']
        start_time = datetime.utcnow()
        print(start_time)

        for earthquake in [e['properties'] for e in earthquakes]:
            tweet_text = "Magnitude {0} earthquake {1}\n{2}".format(earthquake['mag'], earthquake['place'], earthquake['url'])
            print(tweet_text)
            twitter.update_status(tweet_text)
            time.sleep(60)

        time.sleep(60)

except Exception as e:
    print("Error ocurred")
    print(e)
