import os


def validate_credentials():
    """This validates presence of Twitter credentials."""
    if 'TWITTER_CONSUMER_KEY' not in os.environ or \
       'TWITTER_CONSUMER_SECRET' not in os.environ or \
       'TWITTER_ACCESS_TOKEN' not in os.environ or \
       'TWITTER_ACCESS_TOKEN_SECRET' not in os.environ or \
       os.environ['TWITTER_CONSUMER_KEY'] == '' or \
       os.environ['TWITTER_CONSUMER_SECRET'] == '' or \
       os.environ['TWITTER_ACCESS_TOKEN'] == '' or \
       os.environ['TWITTER_ACCESS_TOKEN_SECRET'] == '':
        return False
    return True
