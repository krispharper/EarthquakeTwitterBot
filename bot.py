import os
import requests
import tweepy
from datetime import datetime,timedelta
import time

# Get the Twitter access keys from environment variables
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter = tweepy.API(auth)

# Default start_time to one minute ago
start_time = datetime.utcnow() - timedelta(minutes=1)

try:
    # Loop forever
    while True:
        # Construct the USGS API URL by including start_time as a parameter
        usgs_url = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={0}".format(start_time.isoformat())
        print(usgs_url)
        # Get the response and extract the "features" element
        response = requests.get(usgs_url)
        earthquakes = response.json()['features']

        # Reset start_time to the current time so we how far back to pull data on the next iteration of the loop
        start_time = datetime.utcnow()
        print(start_time)

        # Loop through each of the earthquakes that were returned
        for earthquake in [e['properties'] for e in earthquakes]:
            # Construct the tweet
            tweet_text = "Magnitude {0} earthquake {1}\n{2}".format(earthquake['mag'], earthquake['place'], earthquake['url'])
            print(tweet_text)
            # Post it
            twitter.update_status(tweet_text)
            # Sleep for a minute so we don't spam Twitter in case of many earthquakes at once
            time.sleep(60)

        # Sleep for an hour so we don't spam Twitter
        time.sleep(60 * 60)

except Exception as e:
    print("Error ocurred")
    print(e)
