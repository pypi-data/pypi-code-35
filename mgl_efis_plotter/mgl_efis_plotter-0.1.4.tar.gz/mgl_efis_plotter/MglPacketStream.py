import struct
from typing import BinaryIO, List

from .Exceptions import *


class Record(object):
    """
    one 512 byte record from IEFISBB.DAT
    """

    timestamp: int
    buffer: bytearray

    position: int
    eof: bool

    def __init__(self, timestamp: int, buffer: bytearray):
        self.timestamp = timestamp
        self.buffer = buffer
        self.position = 0
        self.eof = False

    def read(self, qty: int) -> bytearray:
        """
        read qty bytes from the record
        :param qty:
        :return: bytearray
        """
        if self.eof:
            raise EndOfRecord()
        remaining = len(self.buffer) - self.position
        if qty < remaining:
            buffer_slice = self.buffer[self.position: self.position + qty]
            self.position += qty
            return buffer_slice
        else:
            self.eof = True
            return self.buffer[self.position:]


class MglPacketStream(object):
    """
    stream of packets (a/k/a records) sent from the MGL iEFIS and stored in IEFISBB.DAT
    """
    filepointer: BinaryIO
    records: List[Record]
    current_record: int
    eof: bool
    unread_buffer: bytearray
    timestamp: int

    RECORDSIZE = 512

    def __init__(self, fp: BinaryIO, min_timestamp: int = 0, max_timestamp: int = 9000000000):
        self.records = []
        self.current_record = 0
        self.eof = False
        self.unread_buffer = bytearray(0)

        self.filepointer = fp
        self._load_records(min_timestamp, max_timestamp)
        self._sort_records()

        # print('Record timestamps:')
        # lastTs = 0
        # for record in self.records:
        #     print('  {ts:,}'.format(ts=record.timestamp))
        #     lastTs = record.timestamp
        # print('*' * 100)

    def _load_records(self, min_timestamp: int, max_timestamp: int) -> None:
        while True:
            buffer = self.filepointer.read(self.RECORDSIZE)
            if 0 == len(buffer):
                return
            (timestamp, buf) = struct.unpack_from('I 508s', buffer)
            if 0 != timestamp and (min_timestamp <= timestamp <= max_timestamp):
                self.records.append(Record(timestamp, bytearray(buf)))

    def _sort_records(self) -> None:
        """
        Reorder the records so that they are in ascending order, so that nothing else has to deal with a flight
        which wraps back to the beginning of the file
        :return:
        """
        for boundary in range(0, len(self.records) - 2):
            if self.records[boundary].timestamp > self.records[boundary + 1].timestamp:
                a = self.records[boundary + 1:]
                b = self.records[:boundary + 1]
                self.records = a + b

    def read(self, qty: int) -> bytearray:
        """
        read qty bytes from the stream, first checking for unread bytes (had been read and then pushed back ito the
        stream) and then reading from as many records as necessary
        :param qty:
        :return: bytearray
        """
        if self.eof:
            raise EndOfFile()

        if 0 < len(self.unread_buffer):
            unread_bytes = min(len(self.unread_buffer), qty)
            buffer = self.unread_buffer[:unread_bytes]
            self.unread_buffer = self.unread_buffer[unread_bytes:]
            if len(buffer) == qty:
                return buffer
        else:
            buffer = bytearray(0)

        still_needed = qty - len(buffer)
        if self.records[self.current_record].eof:
            self._next_record()
        buffer.extend(self.records[self.current_record].read(still_needed))
        self.timestamp = self.records[self.current_record].timestamp
        if len(buffer) == qty:
            return buffer
        else:
            self._next_record()
            still_needed = qty - len(buffer)
            buffer2 = self.read(still_needed)
            buffer.extend(buffer2)
            return buffer

    def _next_record(self) -> None:
        """
        get another record
        :return:
        """
        self.current_record += 1
        if self.current_record >= len(self.records):
            self.eof = True
            raise EndOfFile()

    def unread(self, buffer: int) -> None:
        """
        take back, and store, a few bytes which had been read but were not needed
        :param buffer:
        :return:
        """
        b = bytearray([buffer])
        self.unread_buffer.extend(b)
