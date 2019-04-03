import unittest
from parameterized import parameterized
from grpc_api_client.client import gRPC_API_Client, gRPC_API_Bindings
from grpc_api_client.grpc.sample import API_TEST_PARAMS
from grpc_api_client.grpc.sample import gRPC_API_Test_Fields

def generate_grpc_methods():
    """
    Generate an argument to pass to parameterized gRPC method tests
    """

    # Generate a mock client
    client = gRPC_API_Test_Client.create()

    # Get all API methods and return a list of names
    method_tests = []
    for name, method in client.api:
        method_tests.append([name, method])
    return method_tests

class gRPC_API_Test_Client(object):
    """
    Test client to Docker gRPC server for test runs.
    """
    def __init__(self, secure):

        # Create a secure client or not
        self.secure = secure

    def connect(self):
        """
        Create a channel to the gRPC server for testing.
        """
        options = {
            'ca_cert': API_TEST_PARAMS['ca_cert'],
            'client_cert': API_TEST_PARAMS['client_cert'],
            'client_key': API_TEST_PARAMS['client_key']
        } if self.secure else {}

        # Return a new Dex client
        client = gRPC_API_Client(
            API_TEST_PARAMS['api_proto'],
            API_TEST_PARAMS['api_grpc']
        )
        client.connect(
            API_TEST_PARAMS['host'],
            API_TEST_PARAMS['port'],
            **options
        )
        return client

    @classmethod
    def create(cls, secure=True):
        """
        Construct and return a test gRPC client interface for testing.
        """
        return cls(secure).connect()

class gRPC_API_Client_Test(unittest.TestCase):
    """Tests for `client.py`."""

    def test_create_secure_client(self):
        """ Test creating a new secure client connection. """
        client = gRPC_API_Test_Client.create()
        self.assertIsInstance(client, gRPC_API_Client)

    def test_create_insecure_client(self):
        """ Test creating a new insecure client connection. """
        client = gRPC_API_Test_Client.create(secure=False)
        self.assertIsInstance(client, gRPC_API_Client)

    def test_api_stub(self):
        """ Test generating an instance of the API stub class """
        client = gRPC_API_Test_Client.create()
        self.assertIsInstance(client.interface.stub, client.interface.stub_class)

    @parameterized.expand(generate_grpc_methods())
    def test_grpc_method(self, name, method):
        client = gRPC_API_Test_Client.create()
        output_class = getattr(client.api, name).output.handler
        response = getattr(client.api, name)(**gRPC_API_Test_Fields.create(method))
        self.assertIsInstance(response.protobuf, output_class)
