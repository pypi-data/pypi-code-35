import json
import logging
import subprocess
import sys
from getpass import getpass
from time import sleep

import click
import requests
from requests import RequestException

EXPORTERS_URL = 'http://{}:5050/api/targets/{}/exporters'

KAFKA_PORT = 9092
KAFKA_EXPORTER_PORT = 9308
MYSQL_PORT = 3306
MYSQL_EXPORTER_PORT = 9104
ELASTICSEARCH_PORT = 9300
ELASTICSEARCH_EXPORTER_PORT = 9108
REDIS_PORT = 6379
REDIS_EXPORTER_PORT = 9121

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class DockerError(Exception):
    """ An error occurred while running docker. """
    pass


class DockerExporterError(DockerError):
    """ An error occurred while running docker exporter. """
    pass


def get_exporters(exporter_id: str, host_ip: str) -> list:
    """
    sends a request to the module, hawkeye
    and retrieves a list of names of exporters which will be executed.
    :return: a list of names of exporters
    """
    host_api = EXPORTERS_URL.format(host_ip, exporter_id)
    r = requests.get(host_api)
    exporter_info = json.loads(r.text)['data']

    exporters_to_return = []
    for exporter in exporter_info:
        exporters_to_return.append(exporter['kind'])

    if len(exporters_to_return) <= 0:
        raise ValueError

    return exporters_to_return


def run_exporter_via_docker(exporters: list, mysql_id: str, mysql_pw: str):
    if 'node' in exporters:
        try:
            image_name = 'quay.io/prometheus/node-exporter'
            net_value = 'host'
            pid_value = 'host'
            v_value = '/:/host:ro,rslave'

            docker_command = 'docker run --name="{}" -d --net="{}" --pid="{}" -v "{}" {} --path.rootfs /host' \
                .format('hawkeye-exporter-node', net_value, pid_value, v_value, image_name)
            execute_docker_command(docker_command, 'node')
        except DockerExporterError as e:
            logger.info(e)
        finally:
            sleep(3)

    if 'kafka' in exporters:
        try:
            image_name = 'danielqsj/kafka-exporter'

            docker_command = 'docker run --name="{}" -d -ti -p {}:{} {} --kafka.server=kafka:{}' \
                .format('hawkeye-exporter-kafka', KAFKA_EXPORTER_PORT, KAFKA_PORT, image_name, KAFKA_PORT)
            execute_docker_command(docker_command, 'kafka')
        except DockerExporterError as e:
            logger.info(e)
        finally:
            sleep(3)

    if 'mysql' in exporters:
        try:
            image_name = 'prom/mysqld-exporter'
            network = 'hawkeye-mysql-network'
            data_source_name = '{}:{}@({}:{})'.format(mysql_id, mysql_pw, network, MYSQL_PORT)

            create_docker_network(network)
            docker_command = 'docker run --name="{}" -d -p {}:{} --network {} -e DATA_SOURCE_NAME="{}/" {}' \
                .format('hawkeye-exporter-mysql', MYSQL_EXPORTER_PORT, MYSQL_PORT, network, data_source_name,
                        image_name)
            execute_docker_command(docker_command, 'mysql')
        except DockerExporterError as e:
            logger.info(e)
        finally:
            sleep(3)

    if 'elasticsearch' in exporters:
        try:
            image_name = 'justwatch/elasticsearch_exporter:1.0.2'

            docker_command = 'docker run --name="{}" -d -p {}:{} {}' \
                .format('hawkeye-exporter-elasticsearch', ELASTICSEARCH_PORT, ELASTICSEARCH_PORT, image_name)
            execute_docker_command(docker_command, 'elasticsearch')
        except DockerExporterError as e:
            logger.info(e)
        finally:
            sleep(3)

    if 'redis' in exporters:
        try:
            image_name = 'oliver006/redis_exporter'

            docker_command = 'docker run --name="{}" -d -p {}:{} {}' \
                .format('hawkeye-exporter-redis', REDIS_EXPORTER_PORT, REDIS_PORT, image_name)
            execute_docker_command(docker_command, 'redis')
        except DockerExporterError as e:
            logger.info(e)
        finally:
            sleep(3)


def execute_docker_command(docker_command: str, exporter_name: str):
    exception_message = 'Exception occurred while running docker exporter: [{}]'.format(exporter_name)
    try:
        subprocess.check_call(docker_command, shell=True)
    except subprocess.CalledProcessError as e:
        raise DockerExporterError(exception_message, e)
    else:
        logger.info('running docker exporter for [{}] succeeded!!'.format(exporter_name))


def create_docker_network(network_name: str):
    """
    MySQL exporter needs a mysql network.
    This method creates a mysql network.
    If a network exists already in the same name, an exception will be occurred
    but there's nothing to do when an exception is throwed.
    :param network_name: name of mysql network
    :return:
    """
    exception_message = 'Exception occurred while creating docker network:'
    network_creation_command = 'docker network create {}'.format(network_name)
    try:
        subprocess.check_call(network_creation_command, shell=True)
    except subprocess.CalledProcessError:
        logger.info(exception_message)


@click.command()
@click.option('-tg', '--target-id', required=True, help='An ID of target for monitoring issued from service provider')
@click.option('-ip', '--host-ip', default='localhost', help='The IP of hawkeye host')
def main(target_id: str, host_ip: str):
    try:
        logger.info('Requesting data with Exporter Id: [{}]'.format(target_id))
        exporters = get_exporters(target_id, host_ip)
    except RequestException:
        logger.info('There are some problems while getting the list of exporters. Contact to the package provider.')
    except ValueError:
        logger.info('Server returned an invalid data. Contact to the package provider.')
    else:
        mysql_id = ''
        mysql_pw = ''
        if 'mysql' in exporters:
            print('You selected MySQL as a target of monitoring.')
            mysql_id = input('Enter your MySql ID of monitoring account:')
            mysql_pw = getpass('Enter your MySql Password of monitoring account.')
        logger.info('Executing exporter(s) for {}...'.format(exporters))
        run_exporter_via_docker(exporters, mysql_id, mysql_pw)


if __name__ == '__main__':
    main()
