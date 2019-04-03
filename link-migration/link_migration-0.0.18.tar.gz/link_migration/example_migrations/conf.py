# -*- coding: utf-8 -*-
import requests
import json

from pathlib import Path

ROOT_DIR = 'link_migration.example_migrations'
MIGRATIONS_ABS_PATH = Path(__file__).resolve().parent
MIGRATIONS_DIR = 'link_migration.example_migrations'

DRIVER = 'neo4j'
DRIVER_KWARGS = {'host': 'bolt://localhost:7687', 'auth': ('neo4j', 'password')}
NEO_HOST = 'localhost'
NEO_PORT = '7474'
NEO_USER = 'neo4j'
NEO_PASSWORD = 'password'
NEO_TRANSACTION_URL = f"http://{NEO_HOST}:{NEO_PORT}/db/data/transaction/commit"

NEO_GRAPH = requests.Session()
NEO_GRAPH.headers = {'Content-Type': "application/json"}
NEO_GRAPH.auth = requests.auth.HTTPBasicAuth(NEO_USER, NEO_PASSWORD)


def get_current_version():
    path = "%s/current_version.txt" % MIGRATIONS_ABS_PATH
    with open(path, "r+") as f:
        content = f.read()
    return int(content)


def set_current_version(version):
    path = "%s/current_version.txt" % MIGRATIONS_ABS_PATH
    with open(path, "w") as f:
        content = f.write(f'{version}')
    return int(content)


def post_neo(data=None):
    if not data:
        raise Exception("data keyword argument is required")

    response = NEO_GRAPH.request(
        "POST",
        NEO_TRANSACTION_URL,
        data=data,
        timeout=5
    )

    response_data = json.loads(response.text)

    if response_data.get('errors'):
        raise Exception(f"Encountered Neo4j Error: {response.text}")

    return response_data
