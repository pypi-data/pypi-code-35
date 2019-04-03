class gRPC_API_Client_Settings(object):
    """
    Store connection settings for the client for use in other classes
    and methods.
    """
    def __init__(self, host, port, **kwargs):
        self.host        = host
        self.port        = port
        self.bindings    = kwargs['bindings']
        self.options     = kwargs.get('options', {})
        self.ca_cert     = kwargs.get('ca_cert', None)
        self.client_cert = kwargs.get('client_cert', None)
        self.client_key  = kwargs.get('client_key', None)
