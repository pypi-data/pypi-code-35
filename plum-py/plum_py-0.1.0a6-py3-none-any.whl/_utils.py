# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2019 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from contextlib import contextmanager
from io import BytesIO

from ._dump import Dump

from ._exceptions import (
    ExcessMemoryError,
    ImplementationError,
    InsufficientMemoryError,
    PackError,
    SizeError,
    UnpackError,
)

from ._plum import Plum
from ._plumtype import PlumType


def calcsize(*items):
    """Get size of packed item (in bytes).

    :param items: plum class or instance
    :type items: PlumClass or Plum
    :returns: size in bytes
    :rtype: int
    :raises SizeError: if size varies with instance

    For example:

        >>> from plum import calcsize
        >>> from plum.int.little import UInt16, UInt8
        >>> calcsize(UInt16)
        2
        >>> calcsize(UInt16(0))
        2
        >>> calcsize(UInt8, UInt16)
        3

    """
    nbytes = 0

    for i, item in enumerate(items):
        if isinstance(item, Plum):
            item_nbytes = type(item)._nbytes
            if item_nbytes is None:
                try:
                    # attempt w/o dump for performance
                    memory = bytearray()
                    _pack(memory, 0, (item,), {}, None)
                    item_nbytes = len(memory)
                except Exception:
                    # do it over to include dump in exception message
                    memory = bytearray()
                    _pack(memory, 0, (item,), {}, Dump(access=f'[{i}]'))
                    item_nbytes = len(memory)
                    raise ImplementationError()

        elif isinstance(item, PlumType):
            item_nbytes = item._nbytes
            if item_nbytes is None:
                raise SizeError(f'{item.__name__!r} instance sizes vary')

        else:
            raise TypeError(f'{item!r} is not a plum class or instance')

        nbytes += item_nbytes

    return nbytes


def dump(item):
    """Print packed memory summary.

    :param Plum item: packable/unpacked memory item

    """
    print(getdump(item))


@contextmanager
def exhaust(memory):
    """Verify all memory bytes consumed.

    Provide context manager that verifies that all memory bytes
    were consumed in unpack operations.

    :param memory: memory to unpack
    :type memory: bytes-like (e.g. bytes, bytearray) or binary file

    """
    try:
        # create binary file from bytes or bytearray
        memory = BytesIO(memory)
    except TypeError:
        pass # must already be a binary file

    try:
        yield memory
    finally:
        extra_bytes = memory.read()
        if extra_bytes:
            msg = f'{len(extra_bytes)} unconsumed memory bytes '
            raise ExcessMemoryError(msg, extra_bytes)


def getbytes(memory, offset, nbytes, limit, dump, cls):
    """Get memory bytes.

    :param memory: memory bytes
    :type memory: bytes-like (e.g. bytes, bytearray, etc.) or binary file
    :param int offset: offset into memory
    :param int nbytes: bytes to consume
    :param int limit: max number of bytes to consume
    :param Dump dump: memory summary dump
    :param type cls: plum type of item that consumed bytes are for
    :returns: tuple of (memory bytes, offset, limit)
    :rtype: bytes-like, int, int or None

    """
    if limit is not None:
        nbytes = limit if (nbytes is None or (limit < nbytes)) else nbytes
        limit -= nbytes

    if nbytes is None:
        try:
            chunk = memory[offset:]
        except TypeError:
            chunk = memory.read()
        else:
            offset += len(chunk)

        if dump:
            dump.cls = cls
            dump.memory = chunk

    else:
        start = offset
        offset += nbytes
        try:
            chunk = memory[start: offset]
        except TypeError:
            chunk = memory.read(nbytes)

        if dump:
            dump.cls = cls
            dump.memory = chunk

        if len(chunk) < nbytes:
            if dump:
                dump.value = '<insufficient bytes>'
                if len(chunk) > 16:
                    dump.add_extra_bytes('', chunk)
                else:
                    dump.buffer = chunk

            cls_name = '' if cls is None else f'{cls.__name__} '

            unpack_shortage = (
                f'{nbytes - len(chunk)} too few memory bytes to unpack {cls_name}'
                f'({nbytes} needed, only {len(chunk)} available)')

            raise InsufficientMemoryError(unpack_shortage)

    return chunk, offset, limit


def getdump(item):
    """Get packed memory summary.

    :param Plum item: packable/unpacked memory item
    :param str name: item name (for ``access`` column)
    :returns: summary table of view detailing memory bytes and layout
    :rtype: str

    """
    dump = Dump()
    _pack(bytearray(), 0, (item,), {}, dump)
    dump.access = 'x'
    return dump


'''
def getvalue(view):
    """Convert view into Python built-in form.

    For example, convert a unsigned 16 bit integer
    data memory view to a native Python ``int``:
        > > > from plum.int.le import UInt16
        > > > x = UInt16(0)
        > > > x
        UInt16(0)
        > > > getvalue(x)
        0

    :param Plum view: data memory view
    :returns: value in Python built-in form
    :rtype: object (Python built-in forms)

    """
    return view.__getvalue__()


def initialize(view, *args, **kwargs):
    """Reset data memory view with initializer arguments.

    Set view value and corresponding memory bytes to new
    value using constructor (__init__) arguments.
    For example:

        > > > from plum import initialize
        > > > from plum.int.le import UInt8, UInt16
        > > > x = UInt16('11', base=16)
        > > > x
        UInt16(17)
        > > > initialize(x, 'ff', base=16)
        > > > x
        UInt16(255)

    :param tuple args: initializer positional arguments
    :param dict kwargs: initializer keyword arguments

    """
    view.__initialize__(*args, **kwargs)
'''


def _pack(memory, offset, items, kwargs, dmp):
    try:
        cls = None
        i = 0
        for item in items:
            if isinstance(item, PlumType):
                if cls is None:
                    cls = item
                else:
                    raise TypeError('plum type specified without a value')
            else:
                if dmp:
                    if dmp.access:
                        dmp = dmp.add_row(access=f'[{i}]')
                    else:
                        dmp.access = f'[{i}]'
                if cls is None:
                    cls = type(item)
                    if not isinstance(cls, PlumType):
                        raise TypeError('value specified without a plum type')
                offset = cls.__pack__(memory, offset, item, dmp)
                i += 1
                cls = None

        if cls is not None:
            raise TypeError('plum type specified without a value')

        if kwargs:
            for name, item in kwargs.items():
                if dmp:
                    if dmp.access:
                        dmp = dmp.add_row(access=name)
                    else:
                        dmp.access = name
                if not isinstance(item, Plum):
                    raise TypeError('value specified without a plum type')
                offset = item.__pack__(memory, offset, item, dmp)

    except Exception as exc:
        if dmp:
            raise PackError(
                f"\n\n{dmp if dmp else '<no dump table yet>'}"
                f"\n\nPackError: unexpected {type(exc).__name__} "
                f"exception occurred during pack operation, dump "
                f"above shows interrupted progress, original "
                f"exception traceback appears above this exception's "
                f"traceback"
            ).with_traceback(exc.__traceback__)
        else:
            raise


def pack(*items, **kwargs):
    r"""Pack items and return memory bytes.

    For example:

        >>> from plum import pack
        >>> from plum.int.little import UInt8, UInt16
        >>> pack(UInt8(1), UInt16(2))
        bytearray(b'\x01\x02\x00')
        >>> pack(UInt8, 1, UInt16, 2)
        bytearray(b'\x01\x02\x00')
        >>> pack(m1=UInt8(1), m2=UInt16(2))
        bytearray(b'\x01\x02\x00')

    :param items: packable/unpacked memory items
    :type items: Plum (e.g. UInt8, Array, etc.)
    :param kwargs: packable/unpacked memory items
    :type kwargs: dict of plum instances
    :returns: memory bytes
    :rtype: bytearray

    """
    memory = bytearray()
    try:
        # attempt w/o dump for performance
        _pack(memory, 0, items, kwargs, None)
    except Exception:
        # do it over to include dump in exception message
        _pack(memory, 0, items, kwargs, Dump())
        raise ImplementationError()

    return memory


def pack_and_getdump(*items, **kwargs):
    """Pack items and return memory bytes and summary.

    :param items: packable/unpacked memory items
    :type items: tuple of plum types/values
    :param kwargs: packable/unpacked memory items
    :type kwargs: dict of plum instances
    :returns: memory bytes, packed memory summary
    :rtype: bytearray, Dump

    """
    memory = bytearray()
    dmp = Dump()
    _pack(memory, 0, items, kwargs, dmp)
    return memory, dmp


def pack_into(buffer, offset, *items, **kwargs):
    r"""Pack items into memory bytes.

    For example:

        >>> from io import BytesIO
        >>> from plum import pack_into
        >>> from plum.int.little import UInt8
        >>>
        >>> memory = bytearray(b'\x00\x00\x00')
        >>> pack_into(memory, 1, UInt8, 1)
        >>> memory
        bytearray(b'\x00\x01\x00')
        >>>
        >>> memory = BytesIO(b'\x00\x00\x00')
        >>> pack_into(memory, 1, UInt8(1))
        >>> memory.seek(0)
        0
        >>> memory.read()
        b'\x00\x01\x00'
        >>>
        >>> memory = bytearray(b'\x00\x00\x00\x00')
        >>> pack_into(memory, 1, m1=UInt8(1), m2=UInt8(2))
        >>> memory
        bytearray(b'\x00\x01\x02\x00')

    :param buffer: memory byte buffer
    :type buffer: writeable bytes-like object or binary file
    :param items: packable/unpacked memory items
    :type items: Plum (e.g. UInt8, Array, etc.)
    :param kwargs: packable/unpacked memory items
    :type kwargs: dict of plum instances

    """
    if isinstance(buffer, bytearray):
        memory = buffer
        _offset = offset
    else:
        memory = bytearray()
        _offset = 0

    try:
        # attempt w/o dump for performance
        _pack(memory, _offset, items, kwargs, None)
    except Exception:
        # do it over to include dump in exception message
        _pack(memory, _offset, items, kwargs, Dump())
        raise ImplementationError()

    if memory is not buffer:
        try:
            buffer[offset:offset + len(memory)] = memory
        except TypeError:
            buffer.seek(offset)
            buffer.write(memory)


def pack_into_and_getdump(buffer, offset, *items, **kwargs):
    r"""Pack items into memory bytes and return memory summary.

    For example:

        >>> from io import BytesIO
        >>> from plum import pack_into
        >>> from plum.int.little import UInt8
        >>>
        >>> memory = bytearray(b'\x00\x00\x00')
        >>> pack_into(memory, 1, UInt8, 1)
        >>> memory
        bytearray(b'\x00\x01\x00')
        >>>
        >>> memory = BytesIO(b'\x00\x00\x00')
        >>> pack_into(memory, 1, UInt8(1))
        >>> memory.seek(0)
        0
        >>> memory.read()
        b'\x00\x01\x00'
        >>>
        >>> memory = bytearray(b'\x00\x00\x00\x00')
        >>> pack_into(memory, 1, m1=UInt8(1), m2=UInt8(2))
        >>> memory
        bytearray(b'\x00\x01\x02\x00')

    :param buffer: memory byte buffer
    :type buffer: writeable bytes-like object or binary file
    :param items: packable/unpacked memory items
    :type items: Plum (e.g. UInt8, Array, etc.)
    :param kwargs: packable/unpacked memory items
    :type kwargs: dict of plum instances
    :returns: packed memory summary
    :rtype: Dump

    """
    if isinstance(buffer, bytearray):
        memory = buffer
        _offset = offset
    else:
        memory = bytearray()
        _offset = 0

    dmp = Dump()

    _pack(memory, _offset, items, kwargs, dmp)

    if memory is not buffer:
        try:
            buffer[offset:offset + len(memory)] = memory
        except TypeError:
            buffer.seek(offset)
            buffer.write(memory)

    return dmp


'''
def setvalue(view, value):
    """Pack value into view data memory.

    For example:
        > > > from plum import setvalue
        > > > from plum.int.le import UInt16
        > > > x = UInt16(0)
        > > > x.setvalue(255)
        > > > x
        UInt16(255)

    :param Plum view: data memory view
    :param object value: new value

    """
    view.__setvalue__(value)
'''


def unpack(cls, memory):
    r"""Unpack item from memory bytes.

    For example:
        >>> from plum import unpack
        >>> from plum.int.little import UInt16
        >>> unpack(UInt16, b'\x01\x02')
        513

    :param PlumClass cls: plum type, e.g. ``UInt16``
    :param memory: memory bytes
    :type memory: bytes-like (e.g. bytes, bytearray, etc.)
    :returns: plum instance
    :rtype: cls

    """
    try:
        item, offset, _limit = cls.__unpack__(memory, 0, None, None, None)
    except Exception as exc:
        # do it over to include dump in exception message
        unpack_and_getdump(cls, memory)
        raise ImplementationError()

    extra_bytes = memory[offset:]

    if extra_bytes:
        # do it over to include dump in exception message
        dump = Dump(access='x')

        try:
            cls.__unpack__(memory, 0, None, dump, None)
        except Exception:
            raise ImplementationError()

        for i in range(0, len(extra_bytes), 16):
            dump.add_row(access='<excess memory>', memory=extra_bytes[i:i+16])

        msg = (
            f'\n\n{dump}\n\n'
            f'{len(extra_bytes)} unconsumed memory bytes '
        )

        raise ExcessMemoryError(msg, extra_bytes)

    return item


def unpack_and_getdump(cls, memory):
    """Unpack item from memory bytes and get packed memory summary.

    For example:
        >>> from plum import unpack_and_getdump
        >>> from plum.int.little import UInt16
        >>> x, dmp = unpack_and_getdump(UInt16, b'\x01\x02')
        >>> x
        513
        >>> print(dmp)
        +--------+--------+-------+--------+--------+
        | Offset | Access | Value | Memory | Type   |
        +--------+--------+-------+--------+--------+
        | 0      | x      | 513   | 01 02  | UInt16 |
        +--------+--------+-------+--------+--------+

    :param Plum cls: plum type, e.g. ``UInt16``
    :param memory: memory bytes
    :type memory: bytes-like (e.g. bytes, bytearray, etc.)
    :returns: tuple of (plum instance, summary)
    :rtype: (cls, str)

    """
    dump = Dump(access='x')

    try:
        item, offset, _limit = cls.__unpack__(memory, 0, None, dump, None)

    except InsufficientMemoryError as exc:
        raise InsufficientMemoryError(
            f'\n\n{dump}\n\nInsufficientMemoryError: {exc}, '
            f'dump above shows interrupted progress',
            *exc.args[1:]).with_traceback(exc.__traceback__)

    except Exception as exc:
        raise UnpackError(
            f"\n\n{dump}"
            f"\n\nUnpackError: unexpected {type(exc).__name__} "
            f"exception occurred during unpack operation, "
            f"dump above shows interrupted progress, original "
            f"exception traceback appears above this exception's "
            f"traceback"
        ).with_traceback(exc.__traceback__)

    extra_bytes = memory[offset:]

    if extra_bytes:
        for i in range(0, len(extra_bytes), 16):
            dump.add_row(access='<excess memory>', memory=extra_bytes[i:i+16])

        msg = (
            f'\n\n{dump}\n\n'
            f'{len(extra_bytes)} unconsumed memory bytes '
        )

        raise ExcessMemoryError(msg, extra_bytes)

    return item, dump


def unpack_from(cls, memory, offset=None):
    r"""Unpack item from memory bytes.

    For example:
        >>> from io import BytesIO
        >>> from plum import unpack_from
        >>> from plum.int.little import UInt8
        >>> unpack_from(UInt8, BytesIO(b'\x99\x01\x99'), offset=1)
        1

    :param PlumClass cls: plum type, e.g. ``UInt16``
    :param memory: memory bytes
    :type memory: binary file
    :param int offset: starting byte offset
    :returns: plum instance
    :rtype: cls

    """
    if offset is None:
        offset = memory.tell()
    else:
        memory.seek(offset)

    try:
        item, _offset, _limit = cls.__unpack__(memory, offset, None, None, None)
    except Exception:
        # do it over to include dump in exception message
        memory.seek(offset)
        unpack_from_and_getdump(cls, memory, offset)
        raise ImplementationError()

    return item


def unpack_from_and_getdump(cls, memory, offset=None):
    """Unpack item from memory bytes and get packed memory summary.

    For example:
        >>> from io import BytesIO
        >>> from plum import unpack_from_and_getdump
        >>> from plum.int.little import UInt8
        >>> x, d = unpack_from_and_getdump(UInt8, BytesIO(b'\x99\x01\x99'), offset=1)
        >>> x
        1
        >>> print(d)
        +--------+--------+-------+--------+-------+
        | Offset | Access | Value | Memory | Type  |
        +--------+--------+-------+--------+-------+
        | 0      | x      | 1     | 01     | UInt8 |
        +--------+--------+-------+--------+-------+

    :param Plum cls: plum type, e.g. ``UInt16``
    :param memory: memory bytes
    :type memory: binary file
    :param int offset: starting byte offset (default to current position)
    :returns: tuple of (plum instance, summary)
    :rtype: (cls, str)

    """
    dump = Dump(access='x')

    if offset is None:
        offset = memory.tell()
    else:
        memory.seek(offset)

    try:
        item, _offset, _limit = cls.__unpack__(memory, offset, None, dump, None)

    except InsufficientMemoryError as exc:
        raise InsufficientMemoryError(
            f'\n\n{dump}\n\nInsufficientMemoryError: {exc}, '
            f'dump above shows interrupted progress',
            *exc.args[1:]).with_traceback(exc.__traceback__)

    except Exception as exc:
        raise UnpackError(
            f"\n\n{dump}"
            f"\n\nUnpackError: unexpected {type(exc).__name__} "
            f"exception occurred during unpack operation, "
            f"dump above shows interrupted progress, original "
            f"exception traceback appears above this exception's "
            f"traceback"
        ).with_traceback(exc.__traceback__)

    return item, dump


'''
def view(type, memory, offset):
    """Create view of packed memory bytes.

    For example:
        > > > from plum import Memory, view
        > > > from plum.int.le import UInt8
        > > > memory = Memory(b'001100')
        > > > view(UInt16, memory, offset=1)
        UInt8(17)

    """
    assert isinstance(memory, Memory)
    return type.__new_view__(memory, offset)
'''
