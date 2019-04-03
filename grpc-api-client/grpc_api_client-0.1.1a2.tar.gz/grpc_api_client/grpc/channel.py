import grpc

class gRPC_API_Credentials(object):
    """
    Factory class for generated gRPC credentials.
    """
    @classmethod
    def read_tls_file(cls, file_path):
        if not file_path:
            return None
        with open(file_path, 'rb') as f:
            return f.read()

    @classmethod
    def create_client(cls, ca_cert, client_cert, client_key):
        """
        Create a new ssl_channel_credentials object.

        :param ca_cert: File path to an optional CA certificate
        :type ca_cert: str
        :param client_cert: File path to client certificate
        :type client_cert: str
        :param client_key: File path to a client key
        :type client_key: str
        :rtype: ssl_channel_credentials
        """
        return grpc.ssl_channel_credentials(
            certificate_chain = cls.read_tls_file(client_cert),
            private_key       = cls.read_tls_file(client_key),
            root_certificates = cls.read_tls_file(ca_cert)
        )

    @classmethod
    def create_server(cls, ca_cert, server_cert, server_key):
        """
        Create a new ssl_channel_credentials for a test server.
        """
        return grpc.ssl_server_credentials(
            private_key_certificate_chain_pairs = [
                [
                cls.read_tls_file(server_key),
                cls.read_tls_file(server_cert)
                ]
            ],
            root_certificates = cls.read_tls_file(ca_cert),
            require_client_auth = True
        )


class gRPC_API_Channel(object):
    """
    Channel for connecting to a gRPC server.
    """
    def __init__(self, settings):
        """
        Create a new gRPC channel to the Dex server.

        :param settings: The settings object passed in from creating the interface
        :type settings: gRPC_API_Client_Settings
        """
        self.host = settings.host
        self.port = settings.port

        # The gRPC target (host:port)
        self.target = '{}:{}'.format(settings.host, settings.port)

        # Extra options to pass to the channel
        self.options = settings.options

        # Options to make a secure (TLS) channel
        self.ca_cert = settings.ca_cert
        self.client_key = settings.client_key
        self.client_cert = settings.client_cert

        # Store the channel object
        self._channel = None

    def _connect_secure(self):
        """
        Make a secure connection to the gRPC server.
        """
        credentials = gRPC_API_Credentials.create_client(
            self.ca_cert,
            self.client_cert,
            self.client_key
        )

        # Open and return the channel
        return grpc.secure_channel(self.target, credentials, options=self.options)

    def _connect_insecure(self):
        """
        Make an insecure connection to the gRPC server.
        """
        return grpc.insecure_channel(self.target, options=self.options)

    def connect(self):
        """
        Open a secure (or insecure if no certificates provided) gRPC channel.
        """

        # Must supply client certificate and key for secure channel
        if self.client_cert and self.client_key:
            self._channel = self._connect_secure()

        # Create an insecure channel
        else:
            self._channel = self._connect_insecure()

        # Return the channel
        return self._channel
