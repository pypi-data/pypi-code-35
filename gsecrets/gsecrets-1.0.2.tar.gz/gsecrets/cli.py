import json
import sys
import click
from .client import Client
from .exceptions import SecretNotFound

@click.group()
def cli():
    pass

def parse_vault_location(path):
    sp = path.split("/")
    vault_location = sp[0] + "/" + sp[1]
    path = "/".join(sp[2:])
    return (vault_location, path)

@cli.command()
@click.argument("path")
@click.argument("content")
@click.option("--replace/--no-replace", default=False)
def put(path, content, replace):
    vault_location, path = parse_vault_location(path)
    client = Client(vault_location)
    client.put(path, content, replace)

@cli.command()
@click.argument("path")
def get(path):
    vault_location, path = parse_vault_location(path)
    client = Client(vault_location)
    try:
        secret = client.get(path)
        if type(secret) is dict:
            print(json.dumps(secret))
        else:
            print(secret.decode("utf-8"))
    except SecretNotFound:
        sys.exit("Secret not found")