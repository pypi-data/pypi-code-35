
from neo4j import GraphDatabase

__all__ = [
    'MigrationDriver',
    'Neo4JDriver'
]


class MigrationDriver:

    def __init__(self):
        available = list(AVAILABLE_DRIVERS.keys())
        raise NotImplementedError(f"No driver specified. Please choose from the list: {available}")

    def write(self, *args):
        raise NotImplementedError

    def read(self, *args):
        raise NotImplementedError

    def get_session(self):
        raise NotImplementedError


class Neo4JDriver(MigrationDriver):

    def __init__(self, host: str, auth: tuple):
        self.driver = GraphDatabase.driver(host, auth=auth)
        self.session = self.get_session()

    def write(self, transaction, cypher):
        return transaction.run(cypher)

    def read(self, transaction, cypher):
        return transaction.run(cypher)

    def get_session(self):
        return self.driver.session


AVAILABLE_DRIVERS = {
    'neo4j': Neo4JDriver
}
