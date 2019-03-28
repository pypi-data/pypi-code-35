import socket
from threading import Thread
from pickle import loads, dumps
from os import path
from math import ceil

def opportunistic_wrapper(i):
    try:
        from tqdm import tqdm
        return tqdm(i)
    except ImportError:
        return i

class ChunkSender(object):
    def __init__(
        self,
        filename:str,
        port=5845,
        chunksize=1024,
        timeout=2,
        iterable_wrapper=opportunistic_wrapper
        ):
        """
        Initializes the object.
        Opens the file.
        Prepares the socket.
        """
        self.port = port
        self.chunksize = chunksize
        self.timeout = 2
        self.file = open(filename, "rb")
        self.iterable_wrapper = iterable_wrapper
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sck.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sck.bind(("0.0.0.0", 5846))
        self.socket = sck
    
    def close(self):
        self.socket.close()
        self.file.close()

    def _sendMeta(self):
        size = self.file.seek(0, 2)
        self.file.seek(0)
        fpath, filename = path.split(self.file.name)
        del fpath
        meta = {
            "length": ceil(size / self.chunksize),
            "name": filename
        } 
        self.chunks = meta["length"]
        self.socket.sendto(dumps(meta), ("255.255.255.255", self.port))
    
    def _receiveAcknowledge(self):
        receiverCount = 0
        self.socket.settimeout(self.timeout)
        try:
            while True:
                data, addr = self.socket.recvfrom(1024)
                if data == b"ACK_META":
                    receiverCount = receiverCount + 1
                    print("Recv'd ACK from", addr)
                if data == b"RDY":
                    receiverCount = receiverCount - 1
                    print("Recv'd RDY from", addr)
        except socket.timeout:
            pass
        self.socket.settimeout(None)
        if receiverCount != 0:
            for recvr in self.iterable_wrapper(range(receiverCount)):
                del recvr
                data, addr = self.socket.recvfrom()
                print("Recv'd RDY from", addr)
    
    def _sendAll(self):
        for chunk in range(self.chunks):
            data = self.file.read(self.chunksize)
            self.socket.sendto(dumps((chunk, data)), ("255.255.255.255", self.port))
    
    def _receiveMissed(self):
        self.socket.settimeout(self.timeout)
        self.socket.sendto(b"EOX", ("255.255.255.255", self.port))
        missed = set()
        try:
            while True:
                data, addr = self.socket.recvfrom(1024)
                del addr
                missed.add(int(data))
        except socket.timeout:
            pass
        self.socket.settimeout(None)
        return missed
    
    def _sendChunks(self, chunks):
        for chunk in self.iterable_wrapper(chunks):
            self.file.seek(chunk*self.chunksize)
            self.socket.sendto(
                dumps((chunk, self.file.read(self.chunksize))),
                ("255.255.255.255", self.port)
            )
    
    def run(self):
        self._sendMeta()
        self._receiveAcknowledge()
        self._sendAll()
        missed = self._receiveMissed()
        while len(missed):
            self._sendChunks(missed)
            missed = self._receiveMissed()


def send(filename:str):
    sender = ChunkSender(filename)
    sender.run()
    sender.close()