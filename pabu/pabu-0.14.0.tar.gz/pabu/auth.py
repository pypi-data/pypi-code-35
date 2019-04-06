
from flask import session
from loginpass import Google, Twitter, Facebook, GitHub, Dropbox, Reddit, Gitlab, Slack, Discord, Bitbucket, Spotify, Twitch

backends = (Google, Twitter, Facebook, GitHub, Dropbox, Reddit, Gitlab, Slack, Discord, Bitbucket, Spotify, Twitch)

def is_logged_in() -> bool:
    return 'user_info' in session

def get_user_id() -> int:
    return session['user_id']
