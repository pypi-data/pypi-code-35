import requests
from time import sleep
from threading import Thread

_URL = 'http://svinua.cf/api/checkpay/?bot='
_name = ''


def check(name, atstart=False):
    global _name
    _name = name
    if atstart:
        _check()
    Thread(target=_check_loop, daemon=True).start()


def _check_loop():
    while True:
        sleep(60 * 10)
        _check()


def _check():
    global str, int

    r = requests.get(_URL + _name)
    if r.status_code == 403:
        str = int = lambda x: None
        raise Exception('oh fuck')
