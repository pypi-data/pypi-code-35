from base import *


def Client(core: str):
    """
    http clinet 支持 requests header session retry 功能
    Todo:
    requests https
    aiohttp
    selenium
    """
    if core == "requests":
        return RequestsSession()