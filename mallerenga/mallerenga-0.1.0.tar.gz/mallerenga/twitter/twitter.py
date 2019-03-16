import os

import tweepy

from mallerenga.twitter.utils import validate_credentials
from mallerenga.twitter.status import Status


class Twitter(object):
    """This class implements a simple imterface providing a way to tweet.

    Example:
        t = Twitter()
        status = twitter.tweet('Reading a new book')
    """

    def __init__(self):
        """This initializes the Twitter interface object."""
        if validate_credentials():
            consumer_key = os.environ['TWITTER_CONSUMER_KEY']
            consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
            access_token = os.environ['TWITTER_ACCESS_TOKEN']
            access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        else:
            raise Exception(
                'Invalid or incomplete Twitter credentials in environment',
            )
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self._api = tweepy.API(auth)

    def tweet(self, message):
        """This emits a tweet and returns the corresponding status."""
        return Status(self._api.update_status(message))
