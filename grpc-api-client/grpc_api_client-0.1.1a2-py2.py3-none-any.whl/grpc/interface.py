from grpc_api_client.grpc.channel import gRPC_API_Channel

class gRPC_API_Interface(object):
    """
    Interface for constructing bindings based on the protocol buffers definition.
    """
    def __init__(self, settings):
        """
        Interface to create the gRPC channel and instance of the API stub class.

        :param settings: The settings object passed in from creating the client
        :type settings: gRPC_API_Client_Settings
        """

        # Create the channel
        self.channel = gRPC_API_Channel(settings).connect()

        # Get the gRPC API stub
        self.stub_class = getattr(settings.bindings.grpc, settings.bindings.stub_name)
        self.stub = self.stub_class(self.channel)
