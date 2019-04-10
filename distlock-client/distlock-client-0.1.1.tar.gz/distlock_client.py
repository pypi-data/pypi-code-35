import os
import json
import urllib
import logging
import threading
from contextlib import contextmanager
import requests


logger = logging.getLogger(__name__)


class Lock(object):
    def __init__(self, appName, server, releaseTimeout=60, token=None):
        self.appName = appName
        self.releaseTimeout = releaseTimeout
        self.server = server
        self.acquire_url = urllib.parse.urljoin(server, "./acquire")
        self.release_url = urllib.parse.urljoin(server, "./release")
        self.token = token

    def acquire(self, lockName, releaseTimeout=None):
        releaseTimeout = releaseTimeout or self.releaseTimeout
        params = {
            "appName": self.appName,
            "lockName": lockName,
            "releaseTimeout": releaseTimeout,
        }
        if self.token:
            params["token"] = self.token
        url = urllib.parse.urljoin(self.acquire_url, "?" + urllib.parse.urlencode((params)))
        respone = requests.get(url)
        result = json.loads(respone.content.decode("utf-8"))
        return result["success"]

    def safe_acquire(self, lockName, releaseTimeout=None):
        try:
            success = self.acquire(lockName, releaseTimeout)
        except Exception as e:
            logger.info("acquire lock failed: {0}".format(str(e)))
            success = False
        return success

    def release(self, lockName):
        params = {
            "appName": self.appName,
            "lockName": lockName,
        }
        if self.token:
            params["token"] = self.token
        url = urllib.parse.urljoin(self.release_url, "?" + urllib.parse.urlencode((params)))
        respone = requests.get(url)
        result = json.loads(respone.content.decode("utf-8"))
        return result["success"]

    def safe_release(self, lockName):
        try:
            success = self.release(lockName)
        except Exception as e:
            logger.info("release lock failed: {0}".format(str(e)))
            success = False
        return success


@contextmanager
def distlock(lockObject, lockName, releaseTimeout=None):
    locked = lockObject.safe_acquire(lockName, releaseTimeout)
    yield locked
    if locked:
        lockObject.safe_release(lockName)


def get_app_unique_name(prefix=None):
    if prefix is None:
        prefix = os.sys.argv[0]
    return "{prefix}:{pid}:{tid}".format(prefix=prefix, pid=os.getpid(), tid=threading.get_ident())
