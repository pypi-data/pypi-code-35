import zmq
from zmq_cache_client.zmq_message import Message


class Client:
    _instances = {}

    def __init__(self, addr):
        if Client._instances.get(addr) is not None:
            raise Exception('ZMQ client is a singleton, use Client.get_instance(addr)')
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(addr)
        Client._instances[addr] = self

    @staticmethod
    def get_instance(addr):
        inst = Client._instances.get(addr)
        if inst is not None:
            return inst
        return Client(addr)

    def send_req(self, msg):
        self.socket.send(msg.to_bytes())
        return Message.from_bytes(self.socket.recv())

    def close(self):
        self.socket.close()
