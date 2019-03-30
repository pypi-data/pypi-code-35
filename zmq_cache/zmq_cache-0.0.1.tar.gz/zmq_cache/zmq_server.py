import zmq
from zmq_cache.zmq_message import Message


class Server:
    def __init__(self, addr):
        context = zmq.Context()
        self.socket = context.socket(zmq.ROUTER)
        self.socket.bind(addr)

    def process(self, cache_operation):
        ident, _, req_msg = self.socket.recv_multipart()
        res = cache_operation(Message.from_bytes(req_msg))
        self.socket.send_multipart([ident, b'', res.to_bytes()])

    def close(self):
        self.socket.close()
