from .api import Client


def exchange_token(token):
    return Client().connection_tokens.filter(
        id=token
    ).exchange(
        meta={}
    )
