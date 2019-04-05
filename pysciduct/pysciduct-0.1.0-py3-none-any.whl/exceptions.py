class RPCError(Exception):
    """
    Error raised when an RPC call goes wrong.
    """
    def __init__(self, message, rpc_call=None):
        super().__init__(message)
        self.rpc_call = rpc_call
