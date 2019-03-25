"""The purpose of this module is to provide functionality for interacting with services outside of this package.

These services should not be related to the core data management aspect of the package, and should instead be used
as extra functionality

"""

from requests import post


def stub(*args, **kwargs):
    """Empty function

    Args:
        *args: Takes all non-default args
        **kwargs: Takes all default args
    """
    del args, kwargs  # Stubbed straight out


def slack(webhook_url, m):
    """Send a Slack message to a Slackbot

    Args:
        webhook_url (str): Webhook of Slackbot
        m (str): The message
    """
    post(webhook_url, headers={'Content-Type': 'application/json'}, json={'text': m})
