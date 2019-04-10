# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import codecs

from .. import UnpackError
from .._plum import Plum
from .._utils import getbytes
from ._strtype import StrType


def decode_str_bytes(memory, decoder, zipped_char_bytes, zero_termination=False):
    reset = True
    for i, byte in enumerate(memory):
        if reset:
            char_bytes = []
            zipped_char_bytes.append(['', char_bytes])

        if zero_termination and byte == 0:
            break

        char = decoder.decode(memory[i:i + 1])
        char_bytes.append(byte)

        if char:
            zipped_char_bytes[-1][0] = char
            reset = True

    # raise exception if bytes remain in decoder (character not complete)
    assert not decoder.decode(b'', final=True)


def encode_str_bytes(string, encoder, zipped_char_bytes):
    for char in string:
        zipped_char_bytes.append((char, encoder.encode(char)))

    assert not encoder.encode('', final=True)


def iter_str_rows(zipped_char_bytes):
    row_index = 0
    row_chars, row_bytes = [], []

    for char, char_bytes in zipped_char_bytes:
        if len(char_bytes) + len(row_bytes) > 16:
            yield row_index, ''.join(row_chars), bytearray(row_bytes)
            row_index += len(row_chars)
            row_chars, row_bytes = [], []

        row_chars.append(char)
        row_bytes += char_bytes

    if row_bytes:
        yield row_index, ''.join(row_chars), bytearray(row_bytes)


def add_str_rows_to_dump(dump, zipped_char_bytes, memory=None, string=None):
    nbytes = 0
    nchar = 0
    for index, chars, bytes_ in iter_str_rows(zipped_char_bytes):
        subdump = dump.add_level(access=f'[{index}:{index + len(chars)}]')
        subdump.value = repr(chars)
        subdump.memory = bytes_
        nbytes += len(bytes_)
        nchar += len(chars)

    if memory:
        dump.add_extra_bytes('--error--', memory[nbytes:])

    if string:
        string = string[nchar:]
        access = '--error--'
        for i in range(0, len(string), 16):
            dump.add_level(access).value = repr(string[i:i + 16])
            access = ''


def add_str_memory_to_dump(dump, memory, decoder):
    zipped_char_bytes = []
    try:
        decode_str_bytes(memory, decoder, zipped_char_bytes)
    finally:
        add_str_rows_to_dump(dump, zipped_char_bytes, memory=memory)


def add_str_value_to_dump(dump, string, encoder):
    zipped_char_bytes = []
    try:
        encode_str_bytes(string, encoder, zipped_char_bytes)
    finally:
        add_str_rows_to_dump(dump, zipped_char_bytes, string=string)


class Str(str, Plum, metaclass=StrType):

    """Interpret memory bytes as a string.

    .. code-block:: none

        Str(object='') -> Str
        Str(bytes_or_buffer[, encoding[, errors]]) -> Str
        pack(Str, str) -> bytes
        unpack(Str, bytes_or_buffer) -> Str

    :param object: string like object
    :type object: object or bytes or buffer
    :param str encoding: encoding name (see :mod:`codecs` standard encodings)
    :param str error: (e.g. ``'string'``, ``'ignore'``, ``'replace'``)

    """

    # filled in by metaclass
    _codecs_info = codecs.lookup('utf-8')
    _errors = 'strict'
    _nbytes = None
    _pad = b'\x00'
    _zero_termination = False

    __equivalent__ = str

    @classmethod
    def __unpack__(cls, memory, offset, limit, dump, parent):
        original_offset = offset
        nbytes = cls._nbytes

        chunk, offset, limit = getbytes(memory, offset, nbytes, limit, dump, cls)

        if cls._zero_termination:

            decoder = cls._codecs_info.incrementaldecoder(cls._errors)

            if dump:
                dump.memory = b''

            zipped_char_bytes = []
            try:
                decode_str_bytes(chunk, decoder, zipped_char_bytes, zero_termination=True)
            except UnicodeDecodeError:
                if dump:
                    add_str_rows_to_dump(dump, zipped_char_bytes, memory=chunk)
                raise

            nstr_membytes = len(b''.join(bytes(b) for c, b in zipped_char_bytes))
            termination = chunk[nstr_membytes:nstr_membytes + 1]

            if termination == b'\x00':
                leftover_bytes = chunk[nstr_membytes + 1:]
            else:
                leftover_bytes = chunk[nstr_membytes:]
                termination = b''

            if nbytes is None:
                offset = original_offset + nstr_membytes + len(termination)
                try:
                    seek = memory.seek
                except AttributeError:
                    pass
                else:
                    seek(offset)
                leftover_bytes = b''

            if dump:
                add_str_rows_to_dump(dump, zipped_char_bytes)
                if termination:
                    subdump = dump.add_level(access='--termination--')
                    subdump.memory = bytes(termination)
                if leftover_bytes:
                    dump.add_extra_bytes('--pad--', bytes(leftover_bytes))

            if termination != b'\x00':
                raise UnpackError('no zero termination present')

            self = ''.join(c for c, b in zipped_char_bytes)

        else:
            if dump:
                dump.memory = b''
                add_str_memory_to_dump(dump, chunk, cls._codecs_info.incrementaldecoder(cls._errors))

            self = str(chunk, cls._codecs_info.name, cls._errors)

        return self, offset, limit

    @classmethod
    def __pack__(cls, memory, offset, object, dump):
        if dump:
            dump.cls = cls
            add_str_value_to_dump(dump, object, cls._codecs_info.incrementalencoder(cls._errors))
            if cls._zero_termination:
                subdump = dump.add_level('--termination--')
                subdump.memory = b'\x00'

        chunk = object.encode(cls._codecs_info.name, cls._errors)

        if cls._zero_termination:
            chunk = chunk + b'\x00'

        nbytes = len(chunk)

        limit = cls._nbytes

        if limit is not None:

            if nbytes > limit:
                raise TypeError(
                    f'{cls.__name__} number of string memory bytes ({nbytes}) '
                    f'exceeds limit ({limit})')

            elif nbytes < limit:
                pad = cls._pad * (limit - nbytes)
                chunk += pad

                if dump and pad:
                    dump.add_extra_bytes('--pad--', pad)

        end = offset + nbytes
        memory[offset:end] = chunk

        return end

    __baserepr__ = str
