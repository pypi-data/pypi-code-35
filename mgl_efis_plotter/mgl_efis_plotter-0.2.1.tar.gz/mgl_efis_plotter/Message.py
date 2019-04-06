import binascii
from typing import Dict

from .MessageData import *
from .MglPacketStream import *


class Message(object):
    """
    Message from an MGL EFIS
    """

    timestamp: int

    total_bytes: int
    type: int
    rate: int
    count: int
    version: int
    data: bytearray
    checksum: int

    raw_header: bytearray
    message_data: MessageData

    config: Config

    def __init__(self, timestamp: int, length: int, packet_stream: MglPacketStream, config: Config):
        self.config = config

        self.timestamp = timestamp

        self.total_bytes = 0
        buffer = packet_stream.read(length + 16)
        self.raw_header = buffer[:4]
        (self.type, self.rate, self.count, self.version) = struct.unpack_from('BBBB', buffer, self.total_bytes)
        self.total_bytes += 4

        length += 8
        format_string = '{length}s I'.format(length=length)
        buffer_slice = buffer[self.total_bytes: self.total_bytes + length + 4]
        (self.data, self.checksum) = struct.unpack(format_string, buffer_slice)
        self.total_bytes += length + 4

        self.set_message_data()

        self._verify_checksum()

    def print(self, timestamp_map: Dict[int, datetime.datetime], prefix: str = '') -> None:
        if self.message_data.MESSAGETYPE is not None:
            if self.timestamp in timestamp_map.keys():
                print(prefix, timestamp_map[self.timestamp], end='  ')
            print(self)

    def set_message_data(self) -> None:
        """
        Create the message_data object and parse the data
        :return:
        """
        if PrimaryFlight.MESSAGETYPE == self.type:
            self.message_data = PrimaryFlight(self.data, self.config)
        elif GPS.MESSAGETYPE == self.type:
            self.message_data = GPS(self.data, self.config)
        elif Attitude.MESSAGETYPE == self.type:
            self.message_data = Attitude(self.data, self.config)
        elif EngineData.MESSAGETYPE == self.type:
            self.message_data = EngineData(self.data, self.config)
        else:
            self.message_data = MessageData(self.data, self.config)

    def _verify_checksum(self) -> None:
        buffer = self.raw_header
        buffer.extend(self.message_data.raw_data)
        crc = binascii.crc32(buffer)  # % (1 << 32) # convert to unsigned CRC32
        if crc != self.checksum:
            raise CrcMismatch(self.total_bytes)

    def __str__(self):
        if self.message_data.MESSAGETYPE is None:
            # return 'Message type {type}  {msgData!s}'.format(type=self.type, msgData=self.message_data)
            return 'Message type {type}'.format(type=self.type)
        else:
            return str(self.message_data)


def find_message(packet_stream: MglPacketStream, config: Config) -> Message:
    """
    find the next valid message in the packet stream, checking for DLE STX LEN LENXOR
    :param packet_stream:
    :param config:
    :return: Message
    """
    while True:
        (dle,) = struct.unpack('B', packet_stream.read(1))
        if 0x5 == dle:
            break
    (ste,) = struct.unpack('B', packet_stream.read(1))
    if 0x5 == ste:
        packet_stream.unread(ste)
        return find_message(packet_stream, config)
    if 0x2 != ste:
        return find_message(packet_stream, config)
    (length, lengthXor) = struct.unpack('BB', packet_stream.read(2))
    if length != (lengthXor ^ 0xff):
        return find_message(packet_stream, config)

    message = Message(packet_stream.timestamp, length, packet_stream, config)
    return message
