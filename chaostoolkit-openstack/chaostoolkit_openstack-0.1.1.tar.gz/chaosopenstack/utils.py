import openstack
from chaoslib.types import Configuration, Secrets
from chaosopenstack import connect
from logzero import logger

__all__ = ["get_server"]


def get_server(client, name):
    for server in client.compute.servers():
        if (
            "metadata" in server
            and "name" in server["metadata"]
            and server["metadata"]["name"] == name
        ):
            return server

    logger.error("No server with name {} found".format(name))
    return None


def get_server_list(
    configuration: Configuration = None, secrets: Secrets = None
) -> list:
    client = connect(secrets=secrets)

    servers = []
    for server in client.compute.servers():
        if "metadata" in server and "name" in server["metadata"]:
            servers.append(
                {"name": server["metadata"]["name"], "status": server["status"]}
            )

    return servers


def print_server_list(configuration: Configuration = None, secrets: Secrets = None):
    servers = get_server_list(configuration, secrets)
    logger.info("Servers:")
    for server in servers:
        logger.info("Name: {}, status: {}".format(server["name"], server["status"]))
