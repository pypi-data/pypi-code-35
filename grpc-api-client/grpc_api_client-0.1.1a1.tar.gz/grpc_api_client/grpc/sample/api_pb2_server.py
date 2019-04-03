import grpc
import logging
from sys import stdout
from time import sleep
from pwd import getpwuid
from grp import getgrgid
from stat import ST_MODE
from os import stat as path_stat
from concurrent.futures import ThreadPoolExecutor
from grpc_api_client.grpc.sample import API_TEST_PARAMS as tp
from grpc_api_client.grpc.sample import api_pb2, api_pb2_grpc
from grpc_api_client.grpc.channel import gRPC_API_Credentials

SRV_TARGET='0.0.0.0:5557'

# Create a logger to stdout
log = logging.getLogger(__name__)
output = logging.StreamHandler(stdout)
output.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
output.setLevel(logging.INFO)
log.addHandler(output)
log.setLevel(logging.INFO)

class APITestServicer(api_pb2_grpc.APITestServicer):
    """
    Subclass of the API service stub object.
    """
    def BoolTest(self, request, context):
        log.info('Handling BoolTest: value={}'.format(request.value))
        log.info('Handling BoolTest: values={}'.format(request.values))
        return request

    def StringTest(self, request, context):
        log.info('Handling StringTest: value={}'.format(request.value))
        log.info('Handling StringTest: values={}'.format(request.values))
        return request

    def Int32Test(self, request, context):
        log.info('Handling Int32Test: value={}'.format(request.value))
        log.info('Handling Int32Test: values={}'.format(request.values))
        return request

    def Int64Test(self, request, context):
        log.info('Handling Int64Test: value={}'.format(request.value))
        log.info('Handling Int64Test: values={}'.format(request.values))
        return request

    def Uint32Test(self, request, context):
        log.info('Handling Uint32Test: value={}'.format(request.value))
        log.info('Handling Uint32Test: values={}'.format(request.values))
        return request

    def Uint64Test(self, request, context):
        log.info('Handling Uint64Test: value={}'.format(request.value))
        log.info('Handling Uint64Test: values={}'.format(request.values))
        return request

    def BytesTest(self, request, context):
        log.info('Handling BytesTest: value={}'.format(request.value))
        log.info('Handling BytesTest: values={}'.format(request.values))
        return request

def get_mode_string(target_path):
    return str(oct(path_stat(target_path)[ST_MODE])[-3:])

def get_owner_string(target_path):
    stat_info = path_stat(target_path)
    uid = stat_info.st_uid
    gid = stat_info.st_gid
    user = getpwuid(uid)[0]
    group = getgrgid(gid)[0]
    return '{}:{}'.format(user, group)

def start_test_server():
    """
    Spin up a test Docker server for running the test suite.
    """
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    log.info('Creating server=ThreadPoolExecutor, max_workers=10')

    # Add the servicer
    api_pb2_grpc.add_APITestServicer_to_server(
      APITestServicer(), server)
    log.info('Adding API servicer: {}'.format(APITestServicer))

    # Add a secure port
    server.add_secure_port(SRV_TARGET, gRPC_API_Credentials.create_server(
        tp['ca_cert'],
        tp['server_cert'],
        tp['server_key']
    ))
    log.info('Creating secure channel on {}'.format(SRV_TARGET))
    log.info('ca_cert: {}, owner={}, mode={}'.format(tp['ca_cert'],
        get_owner_string(tp['ca_cert']),
        get_mode_string(tp['ca_cert'])
    ))
    log.info('server_cert: {}, owner={}, mode={}'.format(tp['server_cert'],
        get_owner_string(tp['server_cert']),
        get_mode_string(tp['server_cert'])
    ))
    log.info('server_key: {}, owner={}, mode={}'.format(tp['server_key'],
        get_owner_string(tp['server_key']),
        get_mode_string(tp['server_key'])
    ))

    # Start the server
    server.start()

    # Keep serving requests
    log.info('Server now running on {}'.format(SRV_TARGET))
    while True:
        sleep(1)
