import sys
from os import path
from django.conf import settings
from pymongo import MongoClient

settings.configure(
    MONGO_DB = MongoClient()['mdbsession_test'],
    SESSION_ENGINE='mdbsession.session',
    SESSION_COOKIE_AGE=3,
)
