from requests import post


def stub(*args, **kwargs):
    """Empty function

    Args:
        *args: Takes all non-default args
        **kwargs: Takes all default args
    """
    del args, kwargs  # Stubbed straight out


def slack(webhook_url: str, m: str):
    """Send a Slack message to a Slackbot

    :param webhook_url: Webhook of Slackbot
    :param m: The message
    """

    post(webhook_url, headers={'Content-Type': 'application/json'}, json={'text': m})
