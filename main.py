import csv
import os
import ssl

import pandas as pd
import tweepy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Target user and twwet ID
ACCOUNT = "wxrldprinceii"
TWEET_ID = "1778172190577287567"


def get_tweet_replies(api, account, tweet_id, n_replies):
    replies = []
    cursor = tweepy.Cursor(api.search_tweets, q="to:" + account, result_type="recent", timeout=99999)
    twwets = cursor.items(n_replies)
    for tweet in twwets:
        if hasattr(tweet, "in_reply_to_status_id_str"):
            if tweet.in_reply_to_status_id_str == tweet_id:
                replies.append(tweet)
    return replies


if __name__ == "__main__":
    # Authenticate with Twitter
    ssl._create_default_https_context = ssl._create_unverified_context
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    replies = get_tweet_replies(api, ACCOUNT, TWEET_ID, 1)
    with open("replies_clean.csv", "w") as f:
        csv_writer = csv.DictWriter(f, fieldnames=("user", "text"))
        csv_writer.writeheader()
        for tweet in replies:
            row = {
                "user": tweet.user.screen_name,
                "text": tweet.text.replace("\n", " "),
            }
            csv_writer.writerow(row)
