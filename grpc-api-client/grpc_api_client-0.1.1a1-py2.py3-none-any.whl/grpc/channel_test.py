import unittest

from grpc_api_client.grpc.sample import gRPC_API_Client_Test_Settings
from grpc_api_client.grpc.channel import gRPC_API_Channel

class gRPC_API_Test_Channel(object):
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

class gRPC_API_Channel_Test(unittest.TestCase):
    """Tests for `grpc/channel.py`."""

    def test_create_secure_channel(self):
        """ Test creating a secure gRPC channel """
        channel = gRPC_API_Test_Channel.create()
        self.assertIsInstance(channel, gRPC_API_Channel)

    def test_create_insecure_interface(self):
        """ Test creating an insecure gRPC channel """
        channel = gRPC_API_Test_Channel.create(secure=False)
        self.assertIsInstance(channel, gRPC_API_Channel)
