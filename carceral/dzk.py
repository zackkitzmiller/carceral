import os
import re

import twitter

DRUNKZACKKITZ_TWITTER_HANDLE = "drunkzackkitz"


def get_twitter_dictionary(username):
    api = get_api()
    statuses = api.GetUserTimeline(screen_name=username, count=200)

    dictionary = []
    for s in statuses:
        s.text = re.sub('<[^<]+?>', '', s.text)
        s.text = re.sub(r"http\S+", "", s.text)
        s.text = re.sub('[^a-zA-Z\s]', "", s.text)
        dictionary += s.text.lower().split()
    return dictionary


def get_dzk_dictionary():
    get_twitter_dictionary(DRUNKZACKKITZ_TWITTER_HANDLE)


def get_api():
    api = twitter.Api(
        consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
        access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
        access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SEC')
    )
    api.VerifyCredentials()
    return api
