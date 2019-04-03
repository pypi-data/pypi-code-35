import unittest
from grpc_api_client.grpc.api import gRPC_API_Collection
from grpc_api_client.grpc.sample import gRPC_API_Client_Test_Settings
from grpc_api_client.grpc.channel import gRPC_API_Channel

class gRPC_API_Test_API(object):
    """
    Test channel to Docker gRPC server for test runs.
    """
    def __init__(self, secure):

        # Create a secure interace or not
        self.secure = secure

    def connect(self):
        """
        Create a channel to the gRPC server for testing.
        """
        if self.secure:
            return gRPC_API_Channel(gRPC_API_Client_Test_Settings.secure())
        else:
            return gRPC_API_Channel(gRPC_API_Client_Test_Settings.insecure())

    @classmethod
    def create(cls, secure=True):
        """
        Construct and return a test gRPC client channel for testing.
        """
        return cls(secure).connect()

class gRPC_API_API_Test(unittest.TestCase):
    """Tests for `grpc/api.py`."""

    def test_api_collection(self):
        """ Test creating an instance of gRPC_API_Collection """
        api_collection = gRPC_API_Collection(None)
        self.assertIsInstance(api_collection, gRPC_API_Collection)
