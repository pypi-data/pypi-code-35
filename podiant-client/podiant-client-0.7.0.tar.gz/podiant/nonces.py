from .api import Client


def get(key):
    return Client().nonces.filter(
        id=key
    )
