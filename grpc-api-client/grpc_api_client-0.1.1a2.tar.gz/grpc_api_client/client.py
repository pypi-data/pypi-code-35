from inspect import getmembers, isclass
from importlib import import_module

from grpc_api_client.grpc.bindings import gRPC_API_Bindings
from grpc_api_client.grpc.settings import gRPC_API_Client_Settings
from grpc_api_client.grpc.interface import gRPC_API_Interface
from grpc_api_client.grpc.api import gRPC_API_Collection, gRPC_API_Path

class gRPC_API_Client(object):
    """
    Create a new gRPC client to connect to a gRPC server.
    """
    def __init__(self, api_proto, api_grpc):
        """
        Create a new gRPC API client instance.

        :param api_proto: The module path to your *pb2.py file
        :type api_proto: str
        :param api_grpc: The module path to your *pb2_grpc.py file
        :type api_grpc: str
        :param stub_name: The name of the stub class to instantiate
        :type stub_name: str
        """
        self.bindings = gRPC_API_Bindings(api_proto, api_grpc)

    def disconnect(self):
        """
        Close the connection to the gRPC server.
        """
        self.interface.channel.close()

    def connect(self, host, port, options={}, ca_cert=None, client_cert=None, client_key=None):
        """
        Create a new client channel to a gRPC server.

        :param host: The gRPC server hostname or IP address
        :type host: str
        :param port: The gRPC server port
        :type port: int
        :param options: Any additional gRPC channel options
        :type options: dict
        :param ca_cert: A CA certificate to use when creating a secure channel
        :type ca_cert: str
        :param client_cert: A client certificate to use when creating a secure channel
        :type client_cert: str
        :param client_key:  A client key to use when creating a secure channel
        :type client_key: str
        :rtype: None
        """
        self.settings = gRPC_API_Client_Settings(host, port,
            options = options,
            ca_cert = ca_cert,
            client_cert = client_cert,
            client_key = client_key,
            bindings = self.bindings
        )

        # Create the gRPC interface
        self.interface = gRPC_API_Interface(self.settings)

        # Store the stub instance
        self.settings.bindings.set_stub(self.interface.stub)

        # API object for containing gRPC procedures
        self.api = gRPC_API_Collection(self.settings)

        # Construct the API
        self._construct_api()

    def _construct_api(self):
        """
        Construct API method handlers from the protobuf client stub instance.
        This maps request and response objects to the method for translating arguments
        into the appropriate request object.
        """
        for method in self.bindings.get_service_methods():
            self.api.add(method)
