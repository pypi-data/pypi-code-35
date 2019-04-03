import unittest

from grpc_api_client.grpc.sample import gRPC_API_Client_Test_Settings
from grpc_api_client.grpc.interface import gRPC_API_Interface

class gRPC_API_Test_Interface(object):
    """
    Test interface to Docker gRPC server for test runs.
    """
    def __init__(self, secure):

        # Create a secure interace or not
        self.secure = secure

    def connect(self):
        """
        Create a interface to the gRPC server for testing.
        """
        if self.secure:
            return gRPC_API_Interface(gRPC_API_Client_Test_Settings.secure())
        else:
            return gRPC_API_Interface(gRPC_API_Client_Test_Settings.insecure())

    @classmethod
    def create(cls, secure=True):
        """
        Construct and return a test gRPC client interface for testing.
        """
        return cls(secure).connect()

class gRPC_API_Interface_Test(unittest.TestCase):
    """ Tests for grpc/interface.py """

    def test_create_secure_interface(self):
        """ Test creating a gRPC interface with a secure channel """
        interface = gRPC_API_Test_Interface.create()
        self.assertIsInstance(interface, gRPC_API_Interface)

    def test_create_insecure_interface(self):
        """ Test creating a gRPC interface with an insecure channel """
        interface = gRPC_API_Test_Interface.create(secure=False)
        self.assertIsInstance(interface, gRPC_API_Interface)
